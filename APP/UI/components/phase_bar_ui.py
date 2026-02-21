import pygame
from APP.UI.styles.colors import TEXT_SEC, ACCENT, SUCCESS

class PhaseBarUI:
    def __init__(self, largura_tela, altura_tela, fontes):
        self.fontes = fontes
        self.largura = largura_tela
        self.altura = altura_tela
        # As 5 fases oficiais que você definiu
        self.fases = ["INICIAL", "PRINCIPAL 1", "COMBATE", "PRINCIPAL 2", "FINAL"]

    def draw(self, screen, fase_atual, jogador_ativo_nome):
        """
        Desenha a barra fixa no topo da tela, fora do campo de jogo.
        """
        # 1. Fundo da Barra Superior (Altura fixa de 40 pixels)
        altura_barra = 40
        pygame.draw.rect(screen, (20, 20, 25), (0, 0, self.largura, altura_barra))
        # Linha de separação neon sutil
        pygame.draw.rect(screen, (50, 50, 60), (0, altura_barra - 2, self.largura, 2))

        # 2. Informação do Jogador Ativo (Canto esquerdo)
        txt_turno = self.fontes['label'].render(f"TURNO DE: {jogador_ativo_nome.upper()}", True, SUCCESS)
        screen.blit(txt_turno, (20, (altura_barra // 2) - (txt_turno.get_height() // 2)))

        # 3. Posicionamento das Fases (Centralizado)
        espaco = 145 # Aumentado para melhor leitura
        largura_total_fases = len(self.fases) * espaco
        # Início centralizado, compensando o nome do jogador à esquerda
        start_x = (self.largura // 2) - (largura_total_fases // 2) + 60 

        y_texto = (altura_barra // 2) - 10 # Alinhamento vertical central

        # 4. Renderização das Fases
        for i, fase in enumerate(self.fases):
            x = start_x + (i * espaco)
            
            if fase == fase_atual:
                # Fase Ativa: Texto em destaque com sublinhado neon
                txt = self.fontes['label'].render(fase, True, ACCENT)
                screen.blit(txt, (x, y_texto))
                
                # Barra neon de progresso abaixo da fase atual
                pygame.draw.rect(screen, ACCENT, (x, y_texto + 22, txt.get_width(), 3), border_radius=2)
            else:
                # Fases Inativas: Texto cinza discreto
                txt = self.fontes['status'].render(fase, True, TEXT_SEC)
                screen.blit(txt, (x, y_texto + 2))