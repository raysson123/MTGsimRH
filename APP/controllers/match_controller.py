from APP.domain.models.match_model import MatchModel
from APP.domain.models.player_model import PlayerModel
from APP.domain.services.deck_builder import DeckBuilderService
from APP.domain.services.rule_engine import RuleEngine

class MatchController:
    def __init__(self, ui_manager):
        """
        Orquestrador da Partida.
        Conecta a lógica de regras (RuleEngine) com a interface (UIManager).
        """
        self.match_model = None
        self.ui_manager = ui_manager 
        self.total_players = 2

    def setup_game(self, human_deck_data: dict, nickname: str = "Conjurador"):
        """
        Inicializa os modelos de jogo e prepara os grimórios.
        """
        print(f"[CONTROLLER] Setup da partida para {nickname}...")

        deck_p1 = DeckBuilderService.build_from_json(human_deck_data)
        deck_p2 = DeckBuilderService.build_from_json(human_deck_data)
        
        player_1 = PlayerModel(player_id="P1", name=nickname, deck=deck_p1)
        player_2 = PlayerModel(player_id="P2", name="Oponente 1", deck=deck_p2)
        
        self.match_model = MatchModel(player1=player_1, player2=player_2)
        print(f"[OK] Mesa montada. Aguardando rolagem de iniciativa.")

    def iniciar_partida(self, primeiro_jogador_id: str):
        """
        Chamado PELA MESA após o vencedor do dado ser decidido.
        É aqui que o jogo realmente começa e as cartas são compradas.
        """
        self.match_model.active_player_id = primeiro_jogador_id
        
        p1 = self.match_model.players["P1"]
        p2 = self.match_model.players["P2"]
        
        p1.deck.embaralhar()
        p2.deck.embaralhar()
        
        p1.draw_cards(7)
        p2.draw_cards(7)
        
        self._simular_mesa_bot(p2)
        
        # ========================================================
        # Força o jogo a iniciar na fase PRINCIPAL 1
        # ========================================================
        try:
            self.match_model.current_phase_index = self.match_model.phases.index("PRINCIPAL 1")
        except ValueError:
            pass 

        primeiro_nome = self.match_model.players[primeiro_jogador_id].name
        print(f"\n[TURNO 1] As cartas foram compradas! {primeiro_nome} começa na fase {self.match_model.phase}!")

    # =========================================================
    # SISTEMA DE MULLIGAN E VIEW
    # =========================================================
    def executar_mulligan(self, player_id: str):
        player = self.match_model.players.get(player_id)
        if player:
            player.return_hand_to_deck()
            player.draw_cards(7)
            print(f"[MESA] {player.name} fez Mulligan e comprou 7 novas cartas.")

    def sincronizar_view(self, zonas_view):
        if self.match_model and self.ui_manager:
            self.ui_manager.preparar_mesa_inicial(self.match_model, zonas_view)

    # =========================================================
    # AÇÕES DO JOGADOR (Processamento de Cliques)
    # =========================================================
    def play_land(self, player_id: str, hand_index: int):
        player = self.match_model.players.get(player_id)
        if not player or hand_index >= len(player.hand): return

        card = player.hand[hand_index]
        permitido, motivo = RuleEngine.validar_descida_terreno(self.match_model, player_id, card)
        
        if permitido:
            player.play_land(hand_index)
            if hasattr(player, 'lands_played_this_turn'):
                player.lands_played_this_turn += 1 
            else:
                player.lands_played_this_turn = 1
            print(f"[AÇÃO] {player.name} jogou: {card.name}")
        else:
            print(f"[BLOQUEADO] {motivo}")

    def cast_creature(self, player_id: str, hand_index: int):
        player = self.match_model.players.get(player_id)
        if not player or hand_index >= len(player.hand): return

        card = player.hand[hand_index]
        permitido, motivo = RuleEngine.validar_conjuracao(self.match_model, player_id, card)
        
        if permitido:
            player.cast_creature(hand_index)
            print(f"[AÇÃO] {player.name} conjurou: {card.name}")
        else:
            print(f"[BLOQUEADO] {motivo}")

    def cast_other(self, player_id: str, hand_index: int):
        player = self.match_model.players.get(player_id)
        if not player or hand_index >= len(player.hand): return

        card = player.hand[hand_index]
        permitido, motivo = RuleEngine.validar_conjuracao(self.match_model, player_id, card)
        
        if permitido:
            player.cast_other(hand_index)
            print(f"[AÇÃO] {player.name} usou: {card.name}")
        else:
            print(f"[BLOQUEADO] {motivo}")

    # =========================================================
    # CONTROLE DE FASES E TURNOS
    # =========================================================
    def next_phase(self):
        """
        Avança o ponteiro de fases do MatchModel.
        O próprio MatchModel cuidará de passar o turno e limpar os contadores
        quando chegar no final da última fase.
        """
        self.match_model.next_phase()
        print(f"[TURNO] Fase atual: {self.match_model.phase}")

    def mudar_vida(self, player_id: str, quantidade: int):
        player = self.match_model.players.get(player_id)
        if player:
            if quantidade > 0: player.gain_life(quantidade)
            else: player.take_damage(abs(quantidade))

    def _simular_mesa_bot(self, bot: PlayerModel):
        if len(bot.hand) >= 3:
            bot.battlefield_lands.append(bot.hand.pop())
            bot.battlefield_creatures.append(bot.hand.pop())