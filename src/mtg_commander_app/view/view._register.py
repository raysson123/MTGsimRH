import pygame
from mtg_commander_app.utils.base import ViewComponent
from mtg_commander_app.utils.ui_components import MenuButton

class RegisterDeckView(ViewComponent):
    def __init__(self, screen, controller, storage_manager):
        super().__init__(screen, controller)
        self.storage = storage_manager
        self.font = pygame.font.SysFont("Arial", 25)
        self.status_message = "Aguardando comando..."
        
        # Centralizar botões baseado na largura do ecrã
        screen_width = screen.get_width()
        self.sync_button = MenuButton(screen_width // 2 - 200, 300, 400, 60, "SINCRONIZAR TXT", self.font)
        self.back_button = MenuButton(screen_width // 2 - 200, 450, 400, 60, "VOLTAR", self.font)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.sync_button.update(mouse_pos)
        self.back_button.update(mouse_pos)

        for event in events:
            if self.sync_button.is_clicked(event):
                self.status_message = "A descarregar cartas... aguarde."
                self.draw() 
                pygame.display.flip()
                
                try:
                    # O StorageManager processa o deck.txt
                    self.storage.download_deck_from_txt("deck.txt")
                    self.status_message = "✅ Deck cadastrado com sucesso!"
                    # Forçar o controller a ler o novo database.json
                    self.controller.reload_data() 
                except Exception as e:
                    self.status_message = f"❌ Erro: {str(e)}"

            if self.back_button.is_clicked(event):
                return "MENU" # Informa ao ViewManager para trocar o estado
        return None

    def draw(self):
        self.screen.fill((30, 30, 40)) 
        
        title_surf = self.font.render("CADASTRO DE DECK (MODO OFFLINE)", True, (255, 255, 255))
        self.screen.blit(title_surf, (self.screen.get_width() // 2 - 150, 100))
        
        msg_surf = self.font.render(self.status_message, True, (200, 200, 200))
        self.screen.blit(msg_surf, (100, 200))
        
        self.sync_button.draw(self.screen)
        self.back_button.draw(self.screen)