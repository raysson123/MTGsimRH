import pygame
from mtg_commander_app.view.view_menu import MainMenu
from mtg_commander_app.view.view_register import RegisterDeckView # Verifique o nome do ficheiro

class ViewManager:
    def __init__(self, screen, controller, storage):
        self.screen = screen
        self.controller = controller
        self.storage = storage
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.views = {
            "MENU": MainMenu(self.screen),
            "CADASTRAR": RegisterDeckView(self.screen, self.controller, self.storage)
        }
        self.state = "MENU"

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "MENU"

            current_view = self.views.get(self.state)
            if self.state == "MENU":
                action = current_view.handle_event(events)
                if action == "CADASTRAR": # Nome do botão no seu view_menu.py
                    self.state = "CADASTRAR"
                elif action == "SAIR":
                    self.running = False
            elif current_view:
                # Captura o retorno da view para mudar de estado (ex: clicar em Voltar)
                res = current_view.handle_events(events)
                if res: self.state = res

            self.draw()
            self.clock.tick(60)

    def draw(self):
        self.screen.fill((25, 25, 25))
        if self.state in self.views:
            self.views[self.state].draw()
        pygame.display.flip()