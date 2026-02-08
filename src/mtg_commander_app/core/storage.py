import os
import json
import requests
import time

class MTGStorageManager:
    def __init__(self, json_path="data/database.json", img_dir="data/assets"):
        self.json_path = json_path
        self.img_dir = img_dir
        self.api_url = "https://api.scryfall.com/cards/named?exact="
        
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)

    def download_deck_from_txt(self, txt_path):
        deck_data = {"commander": None, "cards": []}
        
        with open(txt_path, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        for i, card_name in enumerate(lines):
            print(f"Processando: {card_name}...")
            card_info = self._fetch_scryfall_data(card_name)
            
            if card_info:
                # O primeiro da lista no TXT será o Comandante
                if i == 0:
                    deck_data["commander"] = card_info["name"]
                
                # Baixar imagem PNG localmente
                img_path = self._download_image(card_info)
                card_info["local_img"] = img_path
                
                deck_data["cards"].append(card_info)
            
            time.sleep(0.1) # Respeitar API

        with open(self.json_path, 'w', encoding='utf-8') as j:
            json.dump(deck_data, j, indent=4, ensure_ascii=False)
        print("✅ Database JSON e imagens atualizados!")

    def _fetch_scryfall_data(self, name):
        resp = requests.get(f"{self.api_url}{name}")
        if resp.status_code == 200:
            data = resp.json()
            # Filtramos apenas as características que você quer
            return {
                "id": data.get("id"),
                "name": data.get("name"),
                "mana_cost": data.get("mana_cost"),
                "type_line": data.get("type_line"),
                "oracle_text": data.get("oracle_text"),
                "colors": data.get("colors"),
                "color_identity": data.get("color_identity"),
                "image_url": data.get("image_uris", {}).get("png") # URL para o download
            }
        return None

    def _download_image(self, card_info):
        file_path = os.path.join(self.img_dir, f"{card_info['id']}.png")
        if not os.path.exists(file_path):
            img_data = requests.get(card_info["image_url"]).content
            with open(file_path, 'wb') as handler:
                handler.write(img_data)
        return file_path