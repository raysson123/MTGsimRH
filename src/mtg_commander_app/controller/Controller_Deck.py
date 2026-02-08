import json
import os

class DeckController:
    def __init__(self, json_path="data/database.json"):
        self.json_path = json_path
        self.commander = None
        self.cards = []
        self.reload_data()

    def reload_data(self):
        """Carrega os dados se o arquivo existir; caso contrário, limpa o estado."""
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    self.db = json.load(f)
                self.commander = self.db.get("commander")
                self.cards = self.db.get("cards", [])
            except (json.JSONDecodeError, IOError):
                self._set_empty_state()
        else:
            self._set_empty_state()

    def _set_empty_state(self):
        self.commander = None
        self.cards = []

    def has_deck(self):
        """Retorna True apenas se houver um comandante e cartas cadastradas."""
        return self.commander is not None and len(self.cards) > 0