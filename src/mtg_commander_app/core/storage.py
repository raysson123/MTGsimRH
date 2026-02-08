import os
import json
import requests
import time

class MTGStorageManager:
    def __init__(self, json_path="data/database.json", img_dir="data/assets"):
        self.json_path = json_path
        self.img_dir = img_dir
        self.api_url = "https://api.scryfall.com/cards/named?exact="
        
        # Garante que as pastas existam
        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
        os.makedirs(self.img_dir, exist_ok=True)

    def save_deck_details(self, deck_name, commander_name):
        """
        Atualiza ou define o nome do deck e o comandante no banco de dados.
        """
        data = {"deck_name": "Sem Nome", "commander": None, "cards": []}
        
        # Se o arquivo já existe, carrega os dados atuais para não sobrescrever a lista de cartas
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    pass

        data["deck_name"] = deck_name
        data["commander"] = commander_name

        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Detalhes salvos: {deck_name} | Comandante: {commander_name}")

    def download_deck_from_txt(self, txt_path):
        """
        Lê o arquivo .txt, busca dados na Scryfall e salva a lista inicial de cartas.
        """
        if not os.path.exists(txt_path):
            raise FileNotFoundError(f"Arquivo {txt_path} não encontrado!")

        cards_to_save = []
        with open(txt_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        for line in lines:
            # Tenta separar quantidade do nome (Ex: "1 Sol Ring")
            parts = line.split(' ', 1)
            qty = 1
            name = line
            if parts[0].isdigit():
                qty = int(parts[0])
                name = parts[1]

            # Busca na Scryfall API
            response = requests.get(f"{self.api_url}{name}")
            if response.status_code == 200:
                card_data = response.json()
                cards_to_save.append({
                    "name": card_data.get("name"),
                    "mana_cost": card_data.get("mana_cost"),
                    "type_line": card_data.get("type_line"),
                    "image_url": card_data.get("image_uris", {}).get("normal"),
                    "quantity": qty
                })
                # Delay para respeitar limite da API
                time.sleep(0.1)

        # Salva a lista de cartas mantendo os campos de nome e comandante
        db_content = {
            "deck_name": "Novo Deck",
            "commander": None,
            "cards": cards_to_save
        }

        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(db_content, f, indent=4, ensure_ascii=False)

    def get_commander_data(self):
        """Retorna os dados completos do comandante se estiver definido."""
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                commander_name = data.get("commander")
                for card in data.get("cards", []):
                    if card["name"] == commander_name:
                        return card
        return None