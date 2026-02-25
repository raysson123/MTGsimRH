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

        # FALLBACK (Bolinhas coloridas de segurança caso a imagem falhe)
        cores = {'W': (250, 250, 240), 'U': (80, 150, 220), 'B': (40, 40, 40), 
                 'R': (220, 60, 40), 'G': (60, 160, 80), 'C': (140, 140, 140)}
        for tipo, cor in cores.items():
            surf = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(surf, cor, (12, 12), 12)
            pygame.draw.circle(surf, (20, 20, 20), (12, 12), 12, 1) # Borda
            
            # Tenta usar a fonte 'status' ou 'label' como reserva
            fonte_letra = self.fontes.get('status', self.fontes.get('label'))
            letra = fonte_letra.render(tipo, True, (0,0,0) if tipo in ['W','C'] else (255,255,255))
            surf.blit(letra, (12 - letra.get_width()//2, 12 - letra.get_height()//2))
            icones[tipo] = surf
        return icones

    def draw(self, screen, player, area):
        """Desenha a barra centralizada mostrando a Mana Disponível Total do jogador."""
        
        # 1. Pega a piscina de mana flutuante de forma segura
        mana_container = getattr(player, 'mana_pool', {})
        pool_dict = mana_container.pool if hasattr(mana_container, 'pool') else mana_container
        
        y = area.y + 15 
        tipos_mana = ['W', 'U', 'B', 'R', 'G', 'C']
        espacamento = 55
        largura_total = len(tipos_mana) * espacamento
        start_x = area.centerx - (largura_total // 2)
        
        for i, m_type in enumerate(tipos_mana):
            
            # 🔥 PASSO A: Conta a mana que já foi gerada e está no cofre
            qtd_flutuante = pool_dict.get(m_type, 0)
            
            # 🔥 PASSO B: O NOVO RADAR (Conta os terrenos no campo que ainda podem ser usados)
            qtd_terrenos = 0
            for card in getattr(player, 'battlefield_lands', []):
                # Conta apenas se a carta NÃO estiver virada (is_tapped = False)
                if not card.is_tapped:
                    cor = "C" # Padrão incolor
                    nome = card.name.lower()
                    
                    if "plains" in nome or "planície" in nome: cor = "W"
                    elif "island" in nome or "ilha" in nome: cor = "U"
                    elif "swamp" in nome or "pântano" in nome: cor = "B"
                    elif "mountain" in nome or "montanha" in nome: cor = "R"
                    elif "forest" in nome or "floresta" in nome: cor = "G"
                    elif card.color_identity:
                        cor_temp = card.color_identity[0].upper()
                        if cor_temp in tipos_mana: cor = cor_temp
                        
                    if cor == m_type:
                        qtd_terrenos += 1
            
            # 🔥 PASSO C: A SOMA DO PODER DE COMPRA REAL
            total_disponivel = qtd_flutuante + qtd_terrenos
            
            x = start_x + (i * espacamento)
            
            # Desenha o ícone
            icone = self.icones_mana.get(m_type)
            if icone:
                screen.blit(icone, (x, y))
            
            # Desenha a quantidade ao lado do ícone
            cor_qtd = SUCCESS if total_disponivel > 0 else TEXT_SEC
            txt_qtd = self.fontes['label'].render(str(total_disponivel), True, cor_qtd)
            
            # Alinhamento vertical centralizado com o ícone de 24px
            screen.blit(txt_qtd, (x + 28, y + (12 - txt_qtd.get_height() // 2)))