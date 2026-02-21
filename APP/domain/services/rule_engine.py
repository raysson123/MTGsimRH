from typing import Tuple
from APP.domain.models.match_model import MatchModel
from APP.domain.models.card_model import CardModel

class RuleEngine:
    @staticmethod
    def validar_descida_terreno(match: MatchModel, player_id: str, card: CardModel) -> Tuple[bool, str]:
        """
        Regra: 1 terreno por turno, apenas no seu turno e nas fases PRINCIPAIS.
        """
        # 1. É o turno do jogador?
        if match.active_player_id != player_id:
            return False, "Não é o seu turno!"

        # 2. Está na fase correta? (PRINCIPAL 1 ou PRINCIPAL 2)
        if match.phase not in ["PRINCIPAL 1", "PRINCIPAL 2"]:
            return False, f"Você não pode baixar terrenos na fase {match.phase}."

        # 3. Já baixou terreno este turno? 
        player = match.players[player_id]
        if hasattr(player, 'lands_played_this_turn') and player.lands_played_this_turn >= 1:
            return False, "BLOQUEADO: Você já baixou um terreno este turno."

        # 4. É realmente um terreno?
        if not card.is_land:
            return False, f"{card.name} não é um terreno!"

        return True, "Jogada permitida."

    @staticmethod
    def validar_conjuracao(match: MatchModel, player_id: str, card: CardModel) -> Tuple[bool, str]:
        """
        Regra: Verifica custo de mana e tempo (sorcery speed).
        """
        player = match.players[player_id]

        # 1. Checagem de Turno e Fase (Mágicas normais só na Main Phase)
        if match.active_player_id != player_id:
            # Futuro: Aqui entra a exceção para cartas com 'Flash' ou tipo 'Instant'
            return False, "Você só pode conjurar feitiços/criaturas no seu turno."

        # Sincronizado para as Fases em Português
        if match.phase not in ["PRINCIPAL 1", "PRINCIPAL 2"]:
            return False, f"Conjuração permitida apenas nas Fases Principais (Atual: {match.phase})."

        # 2. Checagem de Custo de Mana
        # Soma TODAS as manas disponíveis no pool (W, U, B, R, G, C)
        total_mana_disponivel = sum(player.mana_pool.values())
        
        if total_mana_disponivel < card.cmc:
            return False, f"Mana insuficiente! Você tem {total_mana_disponivel} e precisa de {card.cmc}."

        # Futuro: Criar lógica para descontar a mana exata da cor (W, U, B, R, G) após a validação
        return True, "Mana disponível!"

    @staticmethod
    def pode_atacar(match: MatchModel, player_id: str, creature: CardModel) -> Tuple[bool, str]:
        """
        Regra: Criaturas não podem atacar no turno em que entram (Enjoô de Invocação) ou se estiverem viradas.
        """
        # Sincronizado para a Fase de Combate
        if match.phase != "COMBATE":
            return False, "Você só pode declarar ataque na fase de COMBATE."
            
        if creature.is_tapped:
            return False, "Esta criatura já está virada e não pode atacar."

        # Futuro: Checar 'Summoning Sickness' (se entrou neste turno) e 'Haste' (Ímpeto)
        return True, "Ataque disponível."