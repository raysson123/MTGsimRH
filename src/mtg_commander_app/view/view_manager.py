import pygame
from mtg_commander_app.view.view_menu import MainMenu
from mtg_commander_app.view.view_register import RegisterDeckView 
from mtg_commander_app.view.view_match import MatchView  # Novo Import

class ViewManager:
    def __init__(self, screen, controller, storage):
        self.screen = screen
        self.controller = controller
        self.storage = storage
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Inicialização das views
        self.views = {
            "MENU": MainMenu(self.screen),
            "CADASTRAR": RegisterDeckView(self.screen, self.controller, self.storage),
            "JOGO": MatchView(self.screen, self.controller) # Nova tela de partida
        }
        
        self.state = "MENU"

    def run(self):
        """Loop principal de gestão de estados e eventos."""
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                
                # ESC para emergência (Voltar ao Menu)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "MENU"

            current_view = self.views.get(self.state)
            
            if self.state == "MENU":
                # O Menu processa eventos e retorna o próximo estado
                action = current_view.handle_event(events, has_deck=self.controller.has_deck())
                
                if action == "ABRIR SALA":
                    # Transição para a mesa de jogo
                    self.state = "JOGO"
                    
                elif action == "CADASTRAR" or action == "LISTAR DECK":
                    self.state = "CADASTRAR"
                    
                elif action == "SAIR":
                    self.running = False
                    
            elif current_view:
                # Processa lógica das outras telas (Cadastro ou Jogo)
                # handle_events retorna o próximo estado se houver mudança
                res = current_view.handle_events(events)
                if res:
                    self.state = res
                    # Se voltou do cadastro, recarrega os dados do deck
                    if res == "MENU":
                        self.controller.reload_data()

            self.draw()
            self.clock.tick(60)

    def draw(self):
        """Renderiza a view ativa no ecrã."""
        # Cor de fundo padrão de segurança
        self.screen.fill((25, 25, 25))

        if self.state == "MENU":
            # Passa o status do deck para gerir pop-up interno do menu
            self.views["MENU"].draw(has_deck=self.controller.has_deck())
        elif self.state in self.views:
            self.views[self.state].draw()

        pygame.display.flip()