import pygame
import os
from mtg_commander_app.core.controller import DeckController
from mtg_commander_app.core.storage import MTGStorageManager
from mtg_commander_app.view.view_manager import ViewManager

def main():
    # 1. Garantir que as pastas de dados existam antes de iniciar
    if not os.path.exists("data/assets"):
        os.makedirs("data/assets")

    # 2. Inicialização do Pygame
    pygame.init()
    # Definimos uma resolução compatível com a exibição de cartas
    screen = pygame.display.set_mode((1024, 768)) 
    pygame.display.set_caption("MTG Commander Simulator - RH")

    # 3. Inicialização dos Componentes de Controle e Dados
    # O DeckController lê o banco de dados JSON local
    controller = DeckController(json_path="data/database.json") 
    
    # O StorageManager cuida do download de imagens e dados via Scryfall
    storage = MTGStorageManager(json_path="data/database.json", img_dir="data/assets")

    # 4. Inicialização do Maestro de Visualização (ViewManager)
    # Passamos o controller e o storage para que as telas possam usá-los
    manager = ViewManager(screen, controller, storage)

    # 5. Execução do Loop Principal
    print("Iniciando Gerenciador Commander...")
    manager.run()

    # 6. Finalização limpa
    pygame.quit()

if __name__ == '__main__':
    main()