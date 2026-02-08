import pygame
from mtg_commander_app.utils.base import ViewComponent
from mtg_commander_app.utils.ui_components import MenuButton

class RegisterDeckView(ViewComponent):
    def __init__(self, screen, controller, storage_manager):
        super().__init__(screen, controller)
        self.storage = storage_manager
        self.font = pygame.font.SysFont("Arial", 25)
        self.status_message = "Aguardando comando..."
        
        # Botão para iniciar a sincronização
        self.sync_button = MenuButton(312, 300, 400, 60, "SINCRONIZAR TXT", self.font)
        self.back_button = MenuButton(312, 450, 400, 60, "VOLTAR", self.font)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.sync_button.update(mouse_pos)
        self.back_button.update(mouse_pos)

        for event in events:
            if self.sync_button.is_clicked(event):
                self.status_message = "Baixando cartas e imagens... aguarde."
                self.draw() # Força um desenho para mostrar a mensagem
                pygame.display.flip()
                
                # Aciona o componente de storage para baixar tudo
                try:
                    self.storage.download_deck_from_txt("deck.txt")
                    self.status_message = "✅ Deck cadastrado com sucesso!"
                    # Recarrega os dados no controller principal
                    self.controller.reload_data()
                except Exception as e:
                    self.status_message = f"❌ Erro: {str(e)}"

            if self.back_button.is_clicked(event):
                return "MENU"
        return None

    def draw(self):
        self.screen.fill((30, 30, 40)) # Azul escuro para diferenciar
        
        # Título
        title_surf = self.font.render("CADASTRO DE DECK (OFFLINE MODE)", True, (255, 255, 255))
        self.screen.blit(title_surf, (250, 100))
        
        # Mensagem de Status
        msg_surf = self.font.render(self.status_message, True, (200, 200, 200))
        self.screen.blit(msg_surf, (100, 200))
        
        self.sync_button.draw(self.screen)
        self.back_button.draw(self.screen)