import pygame
from mtg_commander_app.utils.ui_components import MenuButton

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Verdana", 35)
        self.title_font = pygame.font.SysFont("Georgia", 70, bold=True)
        
        # Criando os botões como componentes
        self.buttons = [
            MenuButton(312, 250, 400, 60, "JOGAR", self.font),
            MenuButton(312, 350, 400, 60, "LISTAR DECK", self.font),
            MenuButton(312, 450, 400, 60, "SAIR", self.font)
        ]

    def handle_event(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            # Atualiza o estado visual (hover)
            for btn in self.buttons:
                btn.update(mouse_pos)
            
            # Verifica cliques
            for btn in self.buttons:
                if btn.is_clicked(event):
                    return btn.text # Retorna o nome da ação ("JOGAR", etc)
        return None

    def draw(self):
        # Fundo do menu (pode ser uma imagem PNG que você baixou)
        self.screen.fill((15, 15, 15))
        
        # Título Estilizado
        title_surf = self.title_font.render("COMMANDER", True, (200, 200, 200))
        title_rect = title_surf.get_rect(center=(self.screen.get_width()//2, 100))
        self.screen.blit(title_surf, title_rect)

        # Desenha cada botão componente
        for btn in self.buttons:
            btn.draw(self.screen)