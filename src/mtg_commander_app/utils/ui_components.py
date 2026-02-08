import pygame

class MenuButton:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        
        # Estilos
        self.color_normal = (150, 150, 150)
        self.color_hover = (255, 215, 0) # Dourado
        self.current_color = self.color_normal
        self.is_hovered = False

    def update(self, mouse_pos):
        """Verifica se o mouse está sobre o botão."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.color_hover if self.is_hovered else self.color_normal

    def draw(self, screen):
        """Desenha o texto com efeito de brilho se selecionado."""
        text_surf = self.font.render(self.text, True, self.current_color)
        # Centraliza o texto no retângulo do botão
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # Se estiver com mouse em cima, desenha uma linha embaixo (estilo menu)
        if self.is_hovered:
            pygame.draw.line(screen, self.color_hover, 
                             (text_rect.left, text_rect.bottom + 2), 
                             (text_rect.right, text_rect.bottom + 2), 2)
            
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Retorna True se o botão foi clicado com o botão esquerdo."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False