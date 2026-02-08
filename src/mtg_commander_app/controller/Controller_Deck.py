import json
import os

class DeckController:
    def __init__(self, json_path="data/database.json"):
        self.json_path = json_path
        self.commander = None
        self.cards = []
        self.reload_data()

    def reload_data(self):
        """Tenta carregar os dados se o ficheiro existir, senão inicia vazio."""
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
            self.commander = self.db.get("commander")
            self.cards = self.db.get("cards", [])
        else:
            self.db = {"commander": None, "cards": []}
            self.cards = []

    def get_commander_data(self):
        for card in self.cards:
            if card["name"] == self.commander:
                return card
        return None

    def get_all_cards(self):
        return self.cards