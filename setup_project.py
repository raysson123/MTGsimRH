import os

def create_structure():
    # Nome do projeto
    project_name = "mtg_commander_app"
    
    # Lista de pastas a serem criadas
    folders = [
        f"src/{project_name}/api",
        f"src/{project_name}/core",
        f"src/{project_name}/models",
        f"src/{project_name}/utils",
        "data",
        "tests",
        "docs"
    ]

    # Criar pastas e arquivos __init__.py
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        init_path = os.path.join(folder, "__init__.py")
        with open(init_path, "w") as f:
            pass
        print(f"✔️ Pasta criada: {folder}")

    # Conteúdo básico para o cliente Scryfall
    scryfall_content = """import requests
import time

class ScryfallClient:
    \"\"\"Cliente básico para interagir com a API Scryfall.\"\"\"
    BASE_URL = "https://api.scryfall.com"

    def search_card(self, name: str):
        time.sleep(0.1)  # Respeitando o limite da API
        url = f"{self.BASE_URL}/cards/named?fuzzy={name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
"""

    # Conteúdo básico para o modelo de Carta
    models_content = """from pydantic import BaseModel
from typing import List, Optional

class MTGCard(BaseModel):
    name: str
    mana_cost: Optional[str]
    type_line: str
    oracle_text: Optional[str]
    colors: List[str]
    color_identity: List[str]
    commander_legal: bool
"""

    # Mapeamento de arquivos iniciais
    files = {
        f"src/{project_name}/api/scryfall_client.py": scryfall_content,
        f"src/{project_name}/models/card.py": models_content,
        "requirements.txt": "requests\npydantic\npytest",
        "README.md": f"# {project_name.replace('_', ' ').title()}\\n\\nProjeto para gerenciar decks de Commander usando a API Scryfall.",
        ".gitignore": "venv/\n__pycache__/\n.env\n*.pyc\ndata/*.json",
        "src/main.py": f"from {project_name}.api.scryfall_client import ScryfallClient\\n\\ndef main():\\n    print('Iniciando Gerenciador Commander...')\\n\\nif __name__ == '__main__':\\n    main()"
    }

    # Criar arquivos com conteúdo
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"📄 Arquivo criado: {path}")

    print("\n🚀 Estrutura completa pronta para o combate!")

if __name__ == "__main__":
    create_structure()