import pygame
from mtg_commander_app.utils.ui_components import MenuButton, UIComponents
from mtg_commander_app.utils.style import GameStyle

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.largura, self.altura = self.screen.get_size()
        
        # Inicializa Estilos e Componentes de UI
        self.fontes = GameStyle.get_fonts()
        self.ui = UIComponents(self.largura, self.altura)
        
        # --- Estado Interno ---
        self.nome_sala = ""
        self.total_jogadores = 2
        self.input_ativo = False
        self.mostrar_aviso = False
        
        # --- Configuração do Pop-up Centralizado ---
        cx, cy = self.largura // 2, self.altura // 2
        self.popup_rect = pygame.Rect(cx - 225, cy - 100, 450, 200)
        self.btn_fechar_popup = MenuButton(
            pygame.Rect(cx - 75, cy + 30, 150, 45), 
            "FECHAR", 
            self.fontes['menu']
        )
        
        # --- Inicialização dos Botões de Seleção (Jogadores) ---
        self.btns_jogadores = {}
        for num, rect in self.ui.rects_jogadores.items():
            self.btns_jogadores[num] = MenuButton(rect, str(num), self.fontes['menu'])

        # --- Inicialização dos Botões de Ação ---
        self.btns_acao = [
            MenuButton(self.ui.rect_criar, "ABRIR SALA", self.fontes['menu']),
            MenuButton(self.ui.rect_cadastrar, "CADASTRAR", self.fontes['menu']),
            MenuButton(pygame.Rect(cx - 150, 620, 300, 50), "SAIR", self.fontes['menu'])
        ]

    def handle_event(self, events, has_deck=False):
        """Gerencia interações respeitando o bloqueio do pop-up."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Atualiza hover do botão de fechar se o pop-up estiver ativo
        if self.mostrar_aviso:
            self.btn_fechar_popup.update(mouse_pos)

        for event in events:
            # 1. Controle do Pop-up (Prioridade Total)
            if self.mostrar_aviso:
                if self.btn_fechar_popup.is_clicked(event):
                    self.mostrar_aviso = False
                continue # Bloqueia eventos do menu de fundo

            # 2. Entrada de Texto (Nome da Sala)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.input_ativo = self.ui.campo_texto_sala.collidepoint(event.pos)
            
            if event.type == pygame.KEYDOWN and self.input_ativo:
                if event.key == pygame.K_BACKSPACE:
                    self.nome_sala = self.nome_sala[:-1]
                elif len(self.nome_sala) < 20:
                    self.nome_sala += event.unicode

            # 3. Seleção de Jogadores
            for num, btn in self.btns_jogadores.items():
                btn.update(mouse_pos)
                if btn.is_clicked(event):
                    self.total_jogadores = num

            # 4. Botões de Ação
            for btn in self.btns_acao:
                btn.update(mouse_pos)
                if btn.is_clicked(event):
                    # Validação de Deck para Abrir Sala
                    if btn.text == "ABRIR SALA" and not has_deck:
                        self.mostrar_aviso = True
                        return None
                    return btn.text
        return None

    def draw(self, has_deck=False):
        """Renderiza o menu com a nova identidade visual de MTG."""
        self.screen.fill(GameStyle.COLOR_BG)
        
        # --- Desenho do Título ---
        txt_t = self.fontes['titulo'].render("MTG SIMULATOR", True, GameStyle.COLOR_ACCENT)
        self.screen.blit(txt_t, (self.largura // 2 - txt_t.get_width() // 2, 40))

        # --- Desenho do Campo de Sala ---
        self.ui.desenhar_caixa_texto(
            self.screen, self.ui.campo_texto_sala, 
            self.nome_sala, self.fontes['menu'], 
            self.input_ativo, "Nome da Sala..."
        )

        # --- Desenho dos Botões de Jogadores ---
        for num, btn in self.btns_jogadores.items():
            # Destaca o selecionado com a cor de sucesso (verde)
            btn.is_hovered = (self.total_jogadores == num) 
            btn.draw(self.screen)

        # --- Desenho dos Botões de Ação ---
        for btn in self.btns_acao:
            btn.draw(self.screen)

        # --- Renderização do Pop-up de Aviso ---
        if self.mostrar_aviso:
            # Overlay escura
            overlay = pygame.Surface((self.largura, self.altura))
            overlay.set_alpha(190)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            # Caixa do Pop-up
            pygame.draw.rect(self.screen, (35, 35, 40), self.popup_rect, border_radius=15)
            pygame.draw.rect(self.screen, GameStyle.COLOR_DANGER, self.popup_rect, 3, border_radius=15)
            
            s1 = self.fontes['popup'].render("⚠️ NENHUM DECK ENCONTRADO!", True, (255, 255, 255))
            self.screen.blit(s1, (self.popup_rect.centerx - s1.get_width() // 2, self.popup_rect.y + 40))
            
            self.btn_fechar_popup.draw(self.screen)