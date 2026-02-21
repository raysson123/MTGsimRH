import pygame
import os
from APP.UI.styles.colors import SUCCESS, TEXT_SEC

class ManaBarUI:
    def __init__(self, fontes):
        self.fontes = fontes
        # Já carrega e fatia a imagem assim que o componente é criado
        self.icones_mana = self._carregar_icones()

    def _carregar_icones(self):
        """Corta a sua imagem manas.png automaticamente ou gera bolinhas coloridas se falhar."""
        icones = {}
        caminho_sprite = "assets/img/manas.png"
        
        if os.path.exists(caminho_sprite):
            try:
                img_full = pygame.image.load(caminho_sprite).convert_alpha()
                bbox = img_full.get_bounding_rect()
                if bbox.width > 0 and bbox.height > 0:
                    img_crop = img_full.subsurface(bbox)
                    
                    # Fatiador: 5 colunas x 2 linhas
                    cw = img_crop.get_width() / 5
                    ch = img_crop.get_height() / 2
                    
                    # Mapeamento do seu arquivo (X, Y)
                    mapa = {
                        'W': (0, 0), 'U': (1, 0), 'B': (2, 0),
                        'R': (3, 0), 'G': (4, 0), 'C': (2, 1) 
                    }
                    
                    for tipo, (col, lin) in mapa.items():
                        rect = pygame.Rect(col * cw, lin * ch, cw, ch)
                        pedaco = img_crop.subsurface(rect)
                        icones[tipo] = pygame.transform.smoothscale(pedaco, (24, 24))
                    
                    print("[UI] Ícones de mana fatiados com sucesso pelo ManaBarUI!")
                    return icones
            except Exception as e:
                print(f"[AVISO] Não foi possível fatiar manas.png: {e}")

        # FALLBACK (Bolinhas coloridas de segurança)
        cores = {'W': (250, 250, 240), 'U': (80, 150, 220), 'B': (60, 60, 60), 'R': (220, 60, 40), 'G': (60, 160, 80), 'C': (180, 180, 180)}
        for tipo, cor in cores.items():
            surf = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(surf, cor, (12, 12), 12)
            pygame.draw.circle(surf, (0, 0, 0), (12, 12), 12, 1)
            letra = self.fontes['status'].render(tipo, True, (0,0,0) if tipo in ['W','C'] else (255,255,255))
            surf.blit(letra, (12 - letra.get_width()//2, 12 - letra.get_height()//2))
            icones[tipo] = surf
        return icones

    def draw(self, screen, player, area):
        """Desenha a barra centralizada abaixo do nome do jogador."""
        y = area.y + 30 
        tipos_mana = ['W', 'U', 'B', 'R', 'G', 'C']
        espacamento = 60
        largura_total = len(tipos_mana) * espacamento
        start_x = area.centerx - (largura_total // 2) + 15
        
        for i, m_type in enumerate(tipos_mana):
            qtd = player.mana_pool.get(m_type, 0)
            x = start_x + (i * espacamento)
            
            icone = self.icones_mana[m_type]
            screen.blit(icone, (x, y))
            
            cor_qtd = SUCCESS if qtd > 0 else TEXT_SEC
            txt_qtd = self.fontes['label'].render(str(qtd), True, cor_qtd)
            screen.blit(txt_qtd, (x + 30, y + 2))