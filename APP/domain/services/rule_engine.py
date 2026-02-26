from typing import Tuple
from APP.domain.models.match_model import MatchModel
from APP.domain.models.card_model import CardModel
from APP.domain.models.game_state import Phase

class RuleEngine:
    """
    O Juiz da partida. Contém puramente a lógica e as regras do Magic.
    NÃO TEM NADA DE UI AQUI. Ele apenas avalia as condições do Model.
    """

    @staticmethod
    def validar_descida_terreno(match: MatchModel, player_id: str, card: CardModel) -> Tuple[bool, str]:
        """Regra: 1 terreno por turno, apenas no seu turno e nas fases PRINCIPAIS."""
        if not card.is_land:
            return False, "A carta não é um terreno."

        if match.state.active_player_id != player_id:
            return False, "Não é o seu turno."

        if match.state.current_phase not in [Phase.PRINCIPAL_1, Phase.PRINCIPAL_2]:
            return False, "Terrenos só podem ser descidos nas fases Principais."

        player = match.players[player_id]
        if player.lands_played_this_turn >= 1:
            return False, "Limite de 1 terreno por turno atingido."

        return True, "Jogada legal."

    @staticmethod
    def validar_conjuracao(match: MatchModel, player_id: str, card: CardModel) -> Tuple[bool, str]:
        """Regra: Verifica custo de mana e timing da mágica."""
        player = match.players[player_id]
        fase = match.state.current_phase

        # ==========================================
        # 1. TIMING (Velocidade da Mágica)
        # ==========================================
        is_instant_speed = card.is_instant or card.has_flash
        
        if not is_instant_speed:
            if match.state.active_player_id != player_id:
                return False, "Feitiços, Artefatos e Criaturas normais só podem ser jogados no seu turno."
            if fase not in [Phase.PRINCIPAL_1, Phase.PRINCIPAL_2]:
                return False, "Isso só pode ser conjurado em uma Fase Principal."

        # ==========================================
        # 2. SISTEMA DE MANA COLORIDA CORRETA
        # ==========================================
        # 🔥 A CORREÇÃO: O Juiz agora pergunta para o nosso novo objeto ManaPool!
        if card.parsed_mana_cost:
            if not player.mana_pool.can_pay(card.parsed_mana_cost):
                return False, "Mana insuficiente para cobrir o custo da mágica."
        else:
            # Fallback de segurança: se a carta não tem custo parseado, olha só o CMC geral
            total_mana = player.mana_pool.get_total()
            if total_mana < card.cmc:
                return False, f"Mana insuficiente. Você tem {total_mana} e o custo é {card.cmc}."

        return True, "Mana e Timing OK."

    @staticmethod
    def pode_atacar(match: MatchModel, player_id: str, card: CardModel) -> Tuple[bool, str]:
        """Regra: Verifica enjoo de invocação e estado da carta no combate."""
        if not card.is_creature:
            return False, "Apenas criaturas atacam."
            
        if match.state.active_player_id != player_id:
            return False, "Você não pode atacar no turno do oponente."
            
        if match.state.current_phase != Phase.COMBATE:
            return False, "Ataques só podem ser declarados na fase de COMBATE."
            
        if card.is_tapped:
            return False, "Esta criatura já está virada e não pode atacar."

        if card.turn_entered == match.state.turn_number and not card.has_haste:
            return False, "Criatura com enjoo de invocação (Summoning Sickness) não pode atacar sem Ímpeto."

        return True, "Ataque disponível."