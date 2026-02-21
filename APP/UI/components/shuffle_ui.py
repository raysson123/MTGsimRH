import pygame
import math
import os
from APP.UI.styles.colors import ACCENT

class ShuffleAnimationUI:
    def __init__(self, largura, altura, fontes, card_w, card_h):
        self.largura = largura
        self.altura = altura
        self.fontes = fontes
        self.card_w = card_w
        self.card_h = card_h
        
        self.ativo = False
        self.inicio_tempo = 0
        self.duracao = 1800 # 1.8 segundos de animação
        
        # Carrega o verso da carta
        self.img_verso = None
        caminho = "assets/img/fudo_cards.jpg"
        if os.path.exists(caminho):
            try:
                img = pygame.image.load(caminho).convert_alpha()
                self.img_verso = pygame.transform.smoothscale(img, (card_w, card_h))
            except:
                pass

    def iniciar(self):
        self.ativo = True
        self.inicio_tempo = pygame.time.get_ticks()

    def esta_rodando(self):
        if not self.ativo: return False
        if pygame.time.get_ticks() - self.inicio_tempo > self.duracao:
            self.ativo = False
            return False
        return True

    def draw(self, screen):
        if not self.ativo: return

        cx, cy = self.largura // 2, self.altura // 2
        t = pygame.time.get_ticks() - self.inicio_tempo
        
        # Escurece o fundo
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 230))
        screen.blit(overlay, (0, 0))

        # Cálculo do movimento (Riffle Shuffle)
        deslocamento = abs(math.sin(t * 0.01)) * 100 
        
        # Desenha os montes
        for i in range(3): # Centro
            self._render_card(screen, cx - self.card_w//2, cy - self.card_h//2 - (i*3))
        
        for i in range(5): # Esquerda e Direita
            self._render_card(screen, cx - self.card_w//2 - deslocamento - (i*6), cy - self.card_h//2 - (i*2))
            self._render_card(screen, cx - self.card_w//2 + deslocamento + (i*6), cy - self.card_h//2 - (i*2))

        # Texto de status
        pontos = "." * ((t // 250) % 4)
        txt = self.fontes['titulo'].render(f"EMBARALHANDO{pontos}", True, ACCENT)
        screen.blit(txt, (cx - txt.get_width()//2, cy + self.card_h + 40))

    def _render_card(self, screen, x, y):
        rect = pygame.Rect(x, y, self.card_w, self.card_h)
        if self.img_verso:
            screen.blit(self.img_verso, rect.topleft)
        else:
            pygame.draw.rect(screen, (43, 37, 33), rect, border_radius=6)
        pygame.draw.rect(screen, ACCENT, rect, 1, border_radius=4)