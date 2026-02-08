import pygame
from mtg_commander_app.utils.base import ViewComponent
from mtg_commander_app.utils.ui_components import MenuButton, UIComponents
from mtg_commander_app.utils.style import GameStyle

class RegisterDeckView(ViewComponent):
    def __init__(self, screen, controller, storage_manager):
        super().__init__(screen, controller)
        self.storage = storage_manager
        self.largura, self.altura = self.screen.get_size()
        
        # Carrega estilos e coordenadas do novo sistema
        self.fontes = GameStyle.get_fonts()
        self.ui = UIComponents(self.largura, self.altura)
        
        # --- Estados de Dados ---
        self.nome_deck = ""
        self.commander_selecionado = ""
        self.cartas_carregadas = []
        self.status_message = "Aguardando comando..."
        self.input_ativo_nome = False
        self.input_ativo_commander = False

        # --- Inicialização dos Botões (Usando Rects do UIComponents) ---
        self.sync_button = MenuButton(self.ui.btn_selecionar_arquivo, "1. CARREGAR TXT", self.fontes['menu'])
        self.confirm_button = MenuButton(self.ui.btn_confirmar_cadastro, "2. SALVAR DECK", self.fontes['menu'])
        self.back_button = MenuButton(self.ui.btn_voltar, "VOLTAR", self.fontes['menu'])

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.sync_button.update(mouse_pos)
        self.back_button.update(mouse_pos)
        self.confirm_button.update(mouse_pos)

        for event in events:
            # 1. Controle de Foco nos Inputs
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.input_ativo_nome = self.ui.rect_input_nome_deck.collidepoint(event.pos)
                # Reutilizando espaço para input do comandante (ajustado no draw)
                self.input_ativo_commander = pygame.Rect(self.largura//2 - 150, 380, 300, 40).collidepoint(event.pos)
            
            # 2. Digitação nos Campos
            if event.type == pygame.KEYDOWN:
                if self.input_ativo_nome:
                    if event.key == pygame.K_BACKSPACE: self.nome_deck = self.nome_deck[:-1]
                    else: self.nome_deck += event.unicode
                elif self.input_ativo_commander:
                    if event.key == pygame.K_BACKSPACE: self.commander_selecionado = self.commander_selecionado[:-1]
                    else: self.commander_selecionado += event.unicode

            # 3. Botão Carregar (Sincronizar)
            if self.sync_button.is_clicked(event):
                self.status_message = "Descarregando cartas... aguarde."
                self.draw() 
                pygame.display.flip()
                try:
                    self.storage.download_deck_from_txt("deck.txt")
                    # Após carregar, tenta pegar o primeiro da lista como sugestão de comandante
                    self.controller.reload_data()
                    self.cartas_carregadas = self.controller.get_all_cards()
                    if self.cartas_carregadas:
                        self.commander_selecionado = self.cartas_carregadas[0]['name']
                    self.status_message = "✅ Cartas baixadas! Defina o Comandante abaixo."
                except Exception as e:
                    self.status_message = f"❌ Erro: {str(e)}"

            # 4. Botão Confirmar (Salvar tudo no JSON)
            if self.confirm_button.is_clicked(event):
                if not self.nome_deck or not self.commander_selecionado:
                    self.status_message = "⚠️ Preencha o nome e o comandante!"
                else:
                    # Atualiza o JSON final com os nomes escolhidos
                    self.storage.save_deck_details(self.nome_deck, self.commander_selecionado)
                    self.controller.reload_data()
                    return "MENU"

            if self.back_button.is_clicked(event):
                return "MENU"
        return None

    def draw(self):
        self.screen.fill(GameStyle.COLOR_BG)
        
        # Título
        txt_t = self.fontes['titulo'].render("CADASTRO DE DECK", True, GameStyle.COLOR_ACCENT)
        self.screen.blit(txt_t, (self.largura//2 - txt_t.get_width()//2, 40))
        
        # Input Nome do Deck
        self.ui.desenhar_caixa_texto(self.screen, self.ui.rect_input_nome_deck, 
                                     self.nome_deck, self.fontes['menu'], 
                                     self.input_ativo_nome, "Nome do Deck...")

        # Botão de Sincronizar
        self.sync_button.draw(self.screen)

        # Campo para Definir Comandante (Aparece após carregar cartas)
        if self.cartas_carregadas or self.commander_selecionado:
            label_c = self.fontes['label'].render("Digite o Nome do Comandante:", True, (200, 200, 200))
            self.screen.blit(label_c, (self.largura//2 - 150, 350))
            
            rect_comm = pygame.Rect(self.largura//2 - 150, 380, 300, 40)
            self.ui.desenhar_caixa_texto(self.screen, rect_comm, 
                                         self.commander_selecionado, self.fontes['menu'], 
                                         self.input_ativo_commander, "Ex: Atraxa...")

        # Mensagem de Status
        msg_surf = self.fontes['status'].render(self.status_message, True, (200, 200, 200))
        self.screen.blit(msg_surf, (self.largura//2 - msg_surf.get_width()//2, 430))
        
        # Botões de Ação
        self.confirm_button.draw(self.screen)
        self.back_button.draw(self.screen)