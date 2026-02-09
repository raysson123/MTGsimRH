import pygame
import os
from APP.utils.style import GameStyle
from APP.utils.ui_components import MenuButton

class DeckListView:
    def __init__(self, screen, controller, storage):
        """
        Galeria de Decks estilo "Grid de Cartas" (6x2).
        """
        self.screen = screen
        self.controller = controller
        self.storage = storage
        self.largura, self.altura = screen.get_size()
        self.fontes = GameStyle.get_fonts()
        
        # --- Configuração da Grade (Grid 6x2) ---
        self.cols = 6
        self.rows = 2
        self.max_decks = self.cols * self.rows # 12 decks máximo
        
        # Dimensões da "Carta" (Proporção Magic ~ 2.5 x 3.5)
        self.card_w = 130
        self.card_h = 182
        self.gap_x = 25
        self.gap_y = 40
        
        # Centralização da Grade na Tela
        largura_total_grid = (self.cols * self.card_w) + ((self.cols - 1) * self.gap_x)
        self.start_x = (self.largura - largura_total_grid) // 2
        self.start_y = 160 # Espaço para o título em cima
        
        # --- Dados e Imagens ---
        self.decks = []
        self.imagens_cache = {} # Cache para não carregar disco a cada frame
        self.selected_index = None
        
        # Carrega dados iniciais
        self.recarregar_lista()
        
        # --- Botões ---
        cx = self.largura // 2
        self.btn_jogar = MenuButton(
            pygame.Rect(cx - 100, self.altura - 90, 200, 50), 
            "JOGAR", 
            self.fontes['menu']
        )
        self.btn_voltar = MenuButton(
            pygame.Rect(20, 20, 100, 40), 
            "VOLTAR", 
            self.fontes['menu']
        )

    def recarregar_lista(self):
        """Lê o perfil e carrega as imagens dos comandantes."""
        self.decks = self._carregar_dados_decks()
        self.imagens_cache = {}
        self.selected_index = None
        
        # Pré-carrega imagens para evitar lag no draw()
        for i, deck in enumerate(self.decks):
            if i >= self.max_decks: break
            cmd_nome = deck.get('commander', '')
            self.imagens_cache[i] = self._buscar_imagem_commander(cmd_nome)

    def _carregar_dados_decks(self):
        """Busca a lista crua do JSON."""
        perfil = self.storage.carregar_perfil()
        return perfil.get("decks_info", {}).get("decks", [])

    def _buscar_imagem_commander(self, nome_commander):
        """Tenta encontrar a imagem JPG do comandante nos assets locais."""
        if not nome_commander: return None
        
        # Normaliza o nome para o formato de arquivo (ex: "Teysa Karlov" -> "teysa_karlov")
        nome_arq = nome_commander.replace(" ", "_").lower().replace("/", "") + ".jpg"
        
        # Procura nas pastas mais prováveis para comandantes
        caminhos_possiveis = [
            os.path.join("assets", "cards", "Criaturas", nome_arq),
            os.path.join("assets", "cards", "Legendary", nome_arq), # Caso tenha criado essa pasta
            os.path.join("assets", "cards", "Outros", nome_arq)
        ]
        
        for caminho in caminhos_possiveis:
            if os.path.exists(caminho):
                try:
                    img = pygame.image.load(caminho).convert() # convert() acelera o blit
                    # Escala a imagem para caber no slot da grade
                    return pygame.transform.scale(img, (self.card_w, self.card_h))
                except:
                    pass
        return None

    def handle_events(self, events):
        """Gerencia clique nas cartas da grade."""
        mouse_pos = pygame.mouse.get_pos()
        self.btn_voltar.update(mouse_pos)
        
        if self.selected_index is not None:
            self.btn_jogar.update(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1. Verifica clique nos decks (Grade)
                for i in range(len(self.decks)):
                    if i >= self.max_decks: break
                    
                    # Calcula a posição deste slot
                    col = i % self.cols
                    row = i // self.cols
                    x = self.start_x + col * (self.card_w + self.gap_x)
                    y = self.start_y + row * (self.card_h + self.gap_y)
                    
                    rect_carta = pygame.Rect(x, y, self.card_w, self.card_h)
                    
                    if rect_carta.collidepoint(event.pos):
                        self.selected_index = i
                        # Aqui você pode adicionar um som de "Carta Selecionada"
                
                # 2. Botão Voltar
                if self.btn_voltar.is_clicked(event):
                    return "MENU"
                
                # 3. Botão Jogar
                if self.selected_index is not None and self.btn_jogar.is_clicked(event):
                    deck_escolhido = self.decks[self.selected_index]
                    # Carrega o deck no controlador
                    if hasattr(self.controller, 'carregar_deck_para_jogo'):
                         self.controller.carregar_deck_para_jogo(deck_escolhido['id'])
                    # Fallback: se o método não existir, seta manualmente (menos seguro)
                    else:
                         print(f"Deck Selecionado ID: {deck_escolhido['id']}")
                         
                    return "JOGO"

        return None

    def draw(self):
        """Renderiza a galeria visual."""
        self.screen.fill(GameStyle.COLOR_BG)
        cx = self.largura // 2

        # Título
        txt_titulo = self.fontes['titulo'].render("SUA COLEÇÃO DE DECKS", True, GameStyle.COLOR_ACCENT)
        self.screen.blit(txt_titulo, (cx - txt_titulo.get_width() // 2, 60))
        
        subtitulo = self.fontes['label'].render("Selecione um Comandante para jogar", True, (150, 150, 150))
        self.screen.blit(subtitulo, (cx - subtitulo.get_width() // 2, 110))

        # --- Renderiza a Grade de Cartas ---
        if not self.decks:
            txt_vazio = self.fontes['menu'].render("Nenhum deck encontrado.", True, (100, 100, 100))
            self.screen.blit(txt_vazio, (cx - txt_vazio.get_width() // 2, 350))
        else:
            for i, deck in enumerate(self.decks):
                if i >= self.max_decks: break # Limite de 12
                
                # Cálculo de Posição
                col = i % self.cols
                row = i // self.cols
                x = self.start_x + col * (self.card_w + self.gap_x)
                y = self.start_y + row * (self.card_h + self.gap_y)
                
                rect = pygame.Rect(x, y, self.card_w, self.card_h)
                
                # 1. Desenha a Capa (Imagem do Comandante)
                img = self.imagens_cache.get(i)
                if img:
                    self.screen.blit(img, (x, y))
                else:
                    # Placeholder se não tiver imagem
                    pygame.draw.rect(self.screen, (40, 40, 45), rect)
                    txt_sigla = self.fontes['titulo'].render("?", True, (60, 60, 65))
                    self.screen.blit(txt_sigla, (rect.centerx - txt_sigla.get_width()//2, rect.centery - txt_sigla.get_height()//2))

                # 2. Desenha a Borda (Destaque se selecionado)
                if i == self.selected_index:
                    # Borda Dourada Grossa (Efeito Glow Simples)
                    pygame.draw.rect(self.screen, GameStyle.COLOR_ACCENT, rect.inflate(6, 6), 3, border_radius=4)
                else:
                    # Borda Fina Cinza
                    pygame.draw.rect(self.screen, (20, 20, 20), rect, 1, border_radius=4)

                # 3. Nome do Deck (Pequeno, abaixo da carta)
                nome_deck = deck.get('name', 'Sem Nome')
                if len(nome_deck) > 15: nome_deck = nome_deck[:13] + ".."
                
                cor_txt = GameStyle.COLOR_ACCENT if i == self.selected_index else (200, 200, 200)
                txt_nome = self.fontes['label'].render(nome_deck, True, cor_txt)
                
                # Centraliza texto abaixo da carta
                self.screen.blit(txt_nome, (rect.centerx - txt_nome.get_width() // 2, rect.bottom + 5))

        # Botões
        self.btn_voltar.draw(self.screen)
        if self.selected_index is not None:
            self.btn_jogar.draw(self.screen)