import pygame
from mtg_commander_app.utils.ui_components import MenuButton

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Verdana", 25)
        self.title_font = pygame.font.SysFont("Georgia", 60, bold=True)
        self.warn_font = pygame.font.SysFont("Arial", 20, bold=True)
        
        # --- Estado do Pop-up ---
        self.mostrar_aviso = False
        
        # --- Configuração do Pop-up Centralizado ---
        width, height = self.screen.get_size()
        cx, cy = width // 2, height // 2
        
        self.popup_rect = pygame.Rect(cx - 225, cy - 100, 450, 200)
        self.btn_fechar_popup = MenuButton(cx - 75, cy + 30, 150, 45, "FECHAR", self.font)
        
        # --- Elementos do Menu ---
        self.nome_sala = ""
        self.total_jogadores = 2
        self.input_ativo = False
        self.rect_sala = pygame.Rect(cx - 150, 150, 300, 40)
        
        self.btn_jogadores = {
            2: MenuButton(cx - 110, 220, 60, 40, "2", self.font),
            3: MenuButton(cx - 30, 220, 60, 40, "3", self.font),
            4: MenuButton(cx + 50, 220, 60, 40, "4", self.font)
        }
        
        self.buttons = [
            MenuButton(cx - 200, 350, 400, 50, "ABRIR SALA", self.font),
            MenuButton(cx - 200, 420, 400, 50, "LISTAR DECK", self.font),
            MenuButton(cx - 200, 490, 400, 50, "CADASTRAR", self.font),
            MenuButton(cx - 200, 560, 400, 50, "SAIR", self.font)
        ]

    def handle_event(self, events, has_deck=False):
        """Gerencia os eventos. Se o pop-up estiver aberto, apenas o botão de fechar é processado."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Atualiza o hover do botão de fechar se o aviso estiver ativo
        if self.mostrar_aviso:
            self.btn_fechar_popup.update(mouse_pos)

        for event in events:
            # 1. Lógica do Pop-up (Bloqueia o resto do menu)
            if self.mostrar_aviso:
                if self.btn_fechar_popup.is_clicked(event):
                    self.mostrar_aviso = False
                # Importante: continue processando a lista de eventos, mas ignore os botões de fundo
                continue 

            # 2. Lógica normal dos elementos do Menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.input_ativo = self.rect_sala.collidepoint(event.pos)
            
            if event.type == pygame.KEYDOWN and self.input_ativo:
                if event.key == pygame.K_BACKSPACE:
                    self.nome_sala = self.nome_sala[:-1]
                else:
                    self.nome_sala += event.unicode

            for num, btn in self.btn_jogadores.items():
                btn.update(mouse_pos)
                if btn.is_clicked(event):
                    self.total_jogadores = num

            for btn in self.buttons:
                btn.update(mouse_pos)
                if btn.is_clicked(event):
                    # Dispara o pop-up se tentar abrir sala sem deck
                    if btn.text == "ABRIR SALA" and not has_deck:
                        self.mostrar_aviso = True
                        return None
                    return btn.text
                    
        return None

    def draw(self, has_deck=False):
        """Desenha o menu e o pop-up por cima se ativado."""
        self.screen.fill((20, 20, 25))
        
        # Título
        txt_t = self.title_font.render("MTG SIMULATOR", True, (255, 255, 255))
        self.screen.blit(txt_t, (self.screen.get_width()//2 - txt_t.get_width()//2, 40))

        # Desenha elementos de fundo (Sala, Jogadores, Botões)
        pygame.draw.rect(self.screen, (100, 100, 100), self.rect_sala, 2, border_radius=5)
        
        txt_exibir = self.nome_sala if self.nome_sala else "Nome da Sala..."
        txt_s = self.font.render(txt_exibir, True, (200, 200, 200))
        self.screen.blit(txt_s, (self.rect_sala.x + 10, self.rect_sala.y + 5))

        for btn in self.btn_jogadores.values():
            btn.color_normal = (50, 200, 50) if self.total_jogadores == int(btn.text) else (100, 100, 100)
            btn.draw(self.screen)
            
        for btn in self.buttons:
            btn.draw(self.screen)

        # 3. Renderização do Pop-up (Aparece se mostrar_aviso for True)
        if self.mostrar_aviso:
            overlay = pygame.Surface(self.screen.get_size())
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            pygame.draw.rect(self.screen, (40, 40, 45), self.popup_rect, border_radius=15)
            pygame.draw.rect(self.screen, (200, 50, 50), self.popup_rect, 3, border_radius=15)
            
            s1 = self.warn_font.render("⚠️ NENHUM DECK ENCONTRADO!", True, (255, 255, 255))
            s2 = pygame.font.SysFont("Arial", 16).render("Importe seu deck em 'CADASTRAR'.", True, (200, 200, 200))
            
            self.screen.blit(s1, (self.popup_rect.centerx - s1.get_width()//2, self.popup_rect.y + 40))
            self.screen.blit(s2, (self.popup_rect.centerx - s2.get_width()//2, self.popup_rect.y + 80))
            
            self.btn_fechar_popup.draw(self.screen)