import os
import json

def inicializar_sistema():
    """Gera os diretórios inexistentes e arquivos base na inicialização."""
    # Lista de pastas essenciais
    diretorios = [
        "data/decks",   
        "data/cards",   
        "data/assets",
        "data/cache"    # Adicionada para alinhar com a estrutura vista na imagem
    ]

    for pasta in diretorios:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            # Substituído o emoji por texto simples para evitar erro de encoding
            print(f"[OK] Diretorio secundario gerado: {pasta}")

    # Inicialização do Profiler
    profiler_path = "data/profiler.json"
    if not os.path.exists(profiler_path):
        default_profile = {
            "player_stats": {"total_matches": 0, "wins": 0, "losses": 0},
            "decks_info": {"total_decks": 0, "decks": []}
        }
        with open(profiler_path, 'w', encoding='utf-8') as f:
            json.dump(default_profile, f, indent=4, ensure_ascii=False)
        print("[OK] Arquivo profiler.json inicializado.")