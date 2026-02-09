import pygame
from APP.view.view_menu import MainMenu
from APP.view.view_register_progress import RegisterProgressView 
from APP.view.view_deck_management import RegisterDeckView
from APP.view.view_deck_list import DeckListView  # <--- TELA DE LISTA
from APP.view.view_match import MatchView
from APP.view.view_welcome import WelcomeView
from APP.controller.match_controller import MatchController
from APP.models.match_model import MatchModel

class ViewManager:
    def __init__(self, screen, controller, storage):
        """
        Gerencia a transição entre telas e o ciclo de vida do simulador.
        """
        self.screen = screen
        self.controller = controller  # DeckController principal
        self.storage = storage        # MTGStorageManager
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Inicializa o controlador de partida com seu modelo de dados
        match_model = MatchModel()
        self.match_controller = MatchController(match_model)
        
        # --- Mapeamento Inicial das Views ---
        self.views = {
            "WELCOME": WelcomeView(self.screen, self.controller, self.storage),
            "MENU": MainMenu(self.screen, self.storage),
            "CADASTRAR": RegisterDeckView(self.screen, self.controller, self.storage),
            "LISTA_DECKS": DeckListView(self.screen, self.controller, self.storage), 
            "JOGO": MatchView(self.screen, self.match_controller) 
        }
        
        # --- LÓGICA DE INICIALIZAÇÃO DE PERFIL ---
        if not self.storage.verificar_perfil_existente():
            self.state = "WELCOME"
        else:
            self.state = "MENU"

    def run(self):
        """Loop principal de gestão de eventos e renderização."""
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Atalho ESC: Voltar ao menu (bloqueado em telas críticas)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state not in ["WELCOME", "PROGRESSO", "JOGO"]:
                        self.state = "MENU"

            current_view = self.views.get(self.state)
            if not current_view: continue

            # --- LÓGICA ESPECÍFICA DO MENU ---
            if self.state == "MENU":
                action = current_view.handle_event(events, has_deck=self.controller.has_deck())
                
                if action == "ABRIR SALA":
                    # Configura número de jogadores para a partida
                    self.match_controller.total_players = current_view.total_jogadores
                    # Vai para a lista escolher o deck
                    self._ir_para_lista_decks()
                
                elif action == "MEUS DECKS":
                    # Apenas visualiza a lista (sem configurar partida)
                    self._ir_para_lista_decks()

                elif action == "CADASTRAR":
                    self.state = "CADASTRAR"
                
                elif action == "SAIR":
                    self.running = False
            
            # --- LÓGICA DE TRANSIÇÃO GENÉRICA ---
            else:
                res = current_view.handle_events(events)

                # Tratamento para Cadastro de Deck (Dicionário de dados)
                if isinstance(res, dict) and res.get("acao") == "INICIAR_PROCESSO":
                    self.iniciar_cadastro_com_progresso(res)
                
                # Tratamento para Navegação Simples (Strings)
                elif isinstance(res, str):
                    self.state = res
                    
                    # Se voltar ao menu, recarrega dados globais
                    if res == "MENU":
                        self.controller.reload_data()
                        if hasattr(self.views["MENU"], "atualizar_nickname"):
                            self.views["MENU"].atualizar_nickname()

            self.draw()
            self.clock.tick(60)

    def _ir_para_lista_decks(self):
        """Método auxiliar para carregar a lista e mudar de tela."""
        # Garante que a lista mostre os decks mais recentes
        if hasattr(self.views["LISTA_DECKS"], '_carregar_lista_decks'):
            self.views["LISTA_DECKS"].decks = self.views["LISTA_DECKS"]._carregar_lista_decks()
        self.state = "LISTA_DECKS"

    def iniciar_cadastro_com_progresso(self, dados_deck):
        """
        Instancia a tela de progresso e inicia o download real (Fase 2).
        """
        nome = dados_deck["nome"]
        path = dados_deck["path"]
        commander = dados_deck.get("commander", "")

        progress_view = RegisterProgressView(self.screen, self.storage, nome, path)
        self.state = "PROGRESSO"
        self.views["PROGRESSO"] = progress_view
        
        # Define o comandante no modelo antes de iniciar o download das imagens
        self.controller.model.commander = commander
        progress_view.iniciar_fluxo(self.controller.model)

    def draw(self):
        """Renderiza a interface gráfica da tela ativa."""
        self.screen.fill((15, 15, 18)) # Fundo

        if self.state == "MENU":
            self.views["MENU"].draw(has_deck=self.controller.has_deck())
        elif self.state in self.views:
            self.views[self.state].draw()

        pygame.display.flip()