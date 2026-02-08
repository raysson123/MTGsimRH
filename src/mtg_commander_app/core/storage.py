import os
import json
import requests
import time
from datetime import date

class MTGStorageManager:
    def __init__(self, base_path="data"):
        """Gerencia a persistência de dados e integração com API."""
        self.base_path = base_path
        self.profiler_path = os.path.join(base_path, "profiler.json")
        self.decks_path = os.path.join(base_path, "decks")
        self.cards_path = os.path.join(base_path, "cards")
        self.api_url = "https://api.scryfall.com/cards/named?exact="
        
        os.makedirs(self.decks_path, exist_ok=True)
        os.makedirs(self.cards_path, exist_ok=True)

    def carregar_perfil(self):
        """Lê o perfil do utilizador para exibir no menu."""
        if os.path.exists(self.profiler_path):
            with open(self.profiler_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"player_info": {"nickname": "Conjurador"}, "decks_info": {"decks": []}}

    def download_deck_from_txt(self, caminho_completo):
        """Lê o ficheiro selecionado e extrai dados da API, incluindo o tipo da carta."""
        cards_extracted = []
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            linhas = [l.strip() for l in f if l.strip()]

        for linha in linhas:
            parts = linha.split(' ', 1)
            qty = int(parts[0]) if parts[0].isdigit() else 1
            name = parts[1] if parts[0].isdigit() else linha

            response = requests.get(f"{self.api_url}{name}")
            if response.status_code == 200:
                data = response.json()
                cards_extracted.append({
                    "name": data.get("name"),
                    "type_line": data.get("type_line", ""), # FUNDAMENTAL PARA O FILTRO DE LENDÁRIAS
                    "mana_cost": data.get("mana_cost", ""),
                    "image_url": data.get("image_uris", {}).get("normal"),
                    "quantity": qty
                })
                time.sleep(0.1) # Respeita o limite da API Scryfall
        
        return cards_extracted

    def registrar_novo_deck(self, deck_model):
        """Cria um novo registro e pasta para o deck."""
        perfil = self.carregar_perfil()
        novo_id = len(perfil['decks_info']['decks']) + 1
        
        # Atualiza Profiler
        perfil['decks_info']['decks'].append({
            "id": novo_id, "name": deck_model.name, "created_at": str(date.today())
        })
        with open(self.profiler_path, 'w', encoding='utf-8') as f:
            json.dump(perfil, f, indent=4)

        self._salvar_arquivos_deck(deck_model, f"{novo_id}_{deck_model.deck_id}")

    def update_deck_existente(self, deck_model):
        """Atualiza um deck já existente sobrescrevendo os ficheiros."""
        perfil = self.carregar_perfil()
        # Procura a pasta existente pelo nome/id no profiler
        deck_data = next((d for d in perfil['decks_info']['decks'] if d['name'] == deck_model.name), None)
        
        if deck_data:
            folder_name = f"{deck_data['id']}_{deck_model.deck_id}"
            self._salvar_arquivos_deck(deck_model, folder_name)
            print(f"[OK] Deck {deck_model.name} atualizado.")

    def _salvar_arquivos_deck(self, deck_model, folder_name):
        """Lógica interna para salvar JSONs de configuração e cartas."""
        path_cards = os.path.join(self.cards_path, folder_name)
        os.makedirs(path_cards, exist_ok=True)
        
        # Salva cards_info.json (Dados completos)
        with open(os.path.join(path_cards, "cards_info.json"), 'w', encoding='utf-8') as f:
            json.dump(deck_model.get_full_json(), f, indent=4, ensure_ascii=False)
            
        # Salva config no diretório de decks
        with open(os.path.join(self.decks_path, f"{deck_model.deck_id}.json"), 'w', encoding='utf-8') as f:
            json.dump(deck_model.get_config_data(), f, indent=4, ensure_ascii=False)
    def verificar_perfil_existente(self):
        """
        Verifica se o arquivo profiler.json existe e se contém um nickname válido.
        Retorna True se o perfil estiver configurado, caso contrário, False.
        """
        if os.path.exists(self.profiler_path):
            try:
                with open(self.profiler_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Verifica se a estrutura mínima de player_info e nickname existe
                    if "player_info" in data and data["player_info"].get("nickname"):
                        return True
            except (json.JSONDecodeError, IOError):
                return False
        return False