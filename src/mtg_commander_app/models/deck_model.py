class DeckModel:
    """Modelo de dados para representar um deck de Commander."""
    def __init__(self, name="", commander=None, cards=None):
        self.name = name
        self.commander = commander
        self.cards = cards if cards is not None else []

    def to_dict(self):
        """Converte o modelo para dicionário para salvar no JSON."""
        return {
            "deck_name": self.name,
            "commander": self.commander,
            "cards": self.cards
        }