from typing import List, Dict, Optional
from APP.domain.models.deck_model import DeckModel
from APP.domain.models.card_model import CardModel
from APP.domain.models.mana_model import ManaPool # 🔥 Importando o novo Motor de Mana

class PlayerModel:
    def __init__(self, player_id: str, name: str, deck: DeckModel, starting_life: int = 40):
        """
        Representa um jogador sentado à mesa.
        Gerencia vida, zonas de jogo e delega a gestão de mana para a ManaPool.
        """
        self.player_id = player_id
        self.name = name
        self.deck = deck
        
        # STATUS DO JOGADOR
        self.life: int = starting_life
        self.poison_counters: int = 0
        self.commander_damage: Dict[str, int] = {}
        self.is_alive: bool = True
        
        # 🔥 O NOVO MOTOR DE MANA (Orientado a Objetos)
        self.mana_pool: ManaPool = ManaPool()
        
        # Controle de Regras de Turno
        self.lands_played_this_turn: int = 0

        # ZONAS DE JOGO
        self.hand: List[CardModel] = []
        self.battlefield_creatures: List[CardModel] = []
        self.battlefield_lands: List[CardModel] = []
        self.battlefield_other: List[CardModel] = [] # Artefatos/Encantamentos
        
        self.graveyard: List[CardModel] = []
        self.exile: List[CardModel] = []
        
        # O Comandante fica em uma lista para facilitar o render
        self.commander_zone: List[CardModel] = []
        if self.deck.commander_card:
            self.commander_zone.append(self.deck.commander_card)

    # =========================================================
    # AÇÕES COM CARTAS E MULLIGAN
    # =========================================================
    def return_hand_to_deck(self):
        """Essencial para o sistema de Mulligan."""
        self.deck.library.extend(self.hand)
        self.hand.clear()
        self.deck.embaralhar()
        print(f"[MODEL] {self.name} devolveu a mão e embaralhou o grimório.")

    def draw_cards(self, amount: int = 1):
        """Puxa cartas do DeckModel."""
        drawn_cards = []
        for _ in range(amount):
            card = self.deck.comprar_carta() 
            if card:
                self.hand.append(card)
                drawn_cards.append(card)
            else:
                self.perder_jogo("Tentou comprar de um grimório vazio (Mill).")
                break
        return drawn_cards

    # =========================================================
    # ENTRADA NO CAMPO DE BATALHA
    # =========================================================
    def play_land(self, card_index: int):
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            if card.is_land:
                card = self.hand.pop(card_index)
                card.untap() 
                self.battlefield_lands.append(card)
                return card
        return None

    def cast_creature(self, card_index: int):
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            if card.is_creature:
                card = self.hand.pop(card_index)
                card.untap()
                self.battlefield_creatures.append(card)
                return card
        return None

    def cast_other(self, card_index: int):
        if 0 <= card_index < len(self.hand):
            card = self.hand.pop(card_index)
            card.untap()
            self.battlefield_other.append(card)
            return card
        return None

    # =========================================================
    # GESTÃO DE VIDA E SOLICITAÇÕES DE MANA
    # =========================================================
    def take_damage(self, amount: int):
        self.life -= amount
        if self.life <= 0:
            self.perder_jogo("Pontos de vida chegaram a zero.")

    def perder_jogo(self, motivo: str):
        if self.is_alive:
            self.is_alive = False
            print(f"[MESA] O jogador {self.name} foi ELIMINADO! Motivo: {motivo}")

    # =========================================================
    # 🔥 ESTRUTURA PARA RECEBER SOLICITAÇÕES DE MANA
    # O Player não calcula mais nada, apenas delega para a ManaPool!
    # =========================================================
    def reset_mana_pool(self):
        """Delega a limpeza da mana para o motor."""
        self.mana_pool.clear()

    def add_mana(self, mana_type: str, amount: int = 1):
        """Recebe a mana do terreno e guarda no motor."""
        self.mana_pool.add_mana(mana_type, amount)

    def pay_mana(self, parsed_cost: dict) -> bool:
        """Delega o cálculo complexo de pagamento de mana para o motor."""
        return self.mana_pool.pay_mana(parsed_cost)