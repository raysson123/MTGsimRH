import pygame
from APP.UI.styles.colors import ACCENT

class GrimorioUI:
    def __init__(self, x, y, card_w, card_h, img_verso=None):
        self.rect = pygame.Rect(x, y, card_w, card_h)
        self.img_verso = img_verso
        self.card_w = card_w
        self.card_h = card_h

    def draw(self, screen, quantidade_cartas):
        if quantidade_cartas <= 0:
            # Desenha apenas o contorno se o deck acabar (derrota por Mill)
            pygame.draw.rect(screen, (50, 0, 0), self.rect, 2, border_radius=6)
            return

        # Efeito de "Pilha": desenha 3 retângulos levemente deslocados para parecer um monte
        for i in range(min(3, quantidade_cartas)):
            offset = i * 2
            r = pygame.Rect(self.rect.x + offset, self.rect.y - offset, self.card_w, self.card_h)
            
            if self.img_verso:
                screen.blit(self.img_verso, r.topleft)
            else:
                pygame.draw.rect(screen, (43, 37, 33), r, border_radius=6)
            
            pygame.draw.rect(screen, ACCENT, r, 1, border_radius=6)