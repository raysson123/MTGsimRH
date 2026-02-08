import pygame

class GameStyle:
    # --- [ PALETA DE CORES MTG ] ---
    COLOR_BG = (15, 15, 18)        # Fundo quase preto
    COLOR_CARD_BACK = (43, 37, 33) # Castanho clássico
    COLOR_ACCENT = (200, 180, 100) # Dourado/Bege para detalhes
    COLOR_DANGER = (180, 50, 50)   # Vermelho para avisos/pop-ups
    COLOR_SUCCESS = (50, 150, 50)  # Verde para botões de ação
    COLOR_TEXT_PRIMARY = (240, 240, 240)
    COLOR_TEXT_SEC = (150, 150, 150)

    # --- [ CARREGAMENTO DE FONTES ] ---
    @staticmethod
    def get_fonts():
        """Retorna um dicionário com fontes padronizadas por categoria."""
        # Se não tiver o arquivo .ttf, o Pygame usará a fonte do sistema mais próxima
        return {
            'titulo': pygame.font.SysFont("Georgia", 60, bold=True),
            'menu': pygame.font.SysFont("Verdana", 22),
            'label': pygame.font.SysFont("Verdana", 16, bold=True),
            'status': pygame.font.SysFont("Arial", 14),
            'popup': pygame.font.SysFont("Georgia", 20, italic=True)
        }