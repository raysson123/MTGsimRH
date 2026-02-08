import pygame
import sys
from mtg_commander_app.view.view_menu import MainMenu
#from mtg_commander_app.view.deck_view import DeckListView
#from mtg_commander_app.view.game_view import GameView

class ViewManager:
    def __init__(self, screen, controller):
        self.screen = screen
        self.controller = controller  # Aqui estão os dados do seu JSON e imagens
        self.clock = pygame.time.Clock()
        self.running = True
        
        # 1. Componentizar as Views: Injetamos o controller em cada uma
        self.views = {
            "MENU": MainMenu(self.screen),
       #     "LISTAR": DeckListView(self.screen, self.controller),
           # "JOGAR": GameView(self.screen, self.controller)
        }
        
        # Estado inicial do projeto
        self.state = "MENU"

    def run(self):
        """Loop principal que orquestra todas as visualizações."""
        while self.running:
            # Captura de eventos globais
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Tecla de emergência: ESC sempre volta para o menu
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "MENU"

            # 2. Lógica de Transição de Estados
            current_view = self.views.get(self.state)
            
            if self.state == "MENU":
                # O menu retorna uma string com o nome da próxima tela
                action = current_view.handle_event(events)
                if action:
                    self._process_menu_action(action)
            else:
                # As outras telas (Listar/Jogar) processam seus próprios cliques
                current_view.handle_events(events)

            # 3. Renderização Modular
            self.draw()
            
            self.clock.tick(60) # Mantém 60 FPS estáveis

    def _process_menu_action(self, action):
        """Conecta os nomes dos botões aos estados do ViewManager."""
        if action == "JOGAR":
            self.state = "JOGAR"
        elif action == "LISTAR DECK":
            self.state = "LISTAR"
        elif action == "SAIR":
            self.running = False

    def draw(self):
        """Limpa a tela e chama o desenho do componente ativo."""
        # Fundo padrão (pode ser substituído por uma imagem de fundo)
        self.screen.fill((25, 25, 25)) 

        # Desenha a View atual
        if self.state in self.views:
            self.views[self.state].draw()

        pygame.display.flip()