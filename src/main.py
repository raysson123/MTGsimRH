import pygame
import os
from mtg_commander_app.controller.Controller_Deck import DeckController # Importação corrigida
from mtg_commander_app.core.storage import MTGStorageManager
from mtg_commander_app.view.view_manager import ViewManager

def main():
    # Garantir pastas de dados
    if not os.path.exists("data/assets"):
        os.makedirs("data/assets")

    pygame.init()
    screen = pygame.display.set_mode((1024, 768)) 
    pygame.display.set_caption("MTG Commander Simulator - RH")

    controller = DeckController(json_path="data/database.json") 
    storage = MTGStorageManager(json_path="data/database.json", img_dir="data/assets")

    manager = ViewManager(screen, controller, storage)

    print("Iniciando Gerenciador Commander...")
    manager.run()

    pygame.quit()

if __name__ == '__main__':
    main()