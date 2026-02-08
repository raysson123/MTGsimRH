import pygame
from mtg_commander_app.view.view_menu import MainMenu
from mtg_commander_app.view.view_register import RegisterDeckView 

class ViewManager:
    def __init__(self, screen, controller, storage):
        self.screen = screen
        self.controller = controller
        self.storage = storage
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Inicialização das views com injeção de dependências
        self.views = {
            "MENU": MainMenu(self.screen),
            "CADASTRAR": RegisterDeckView(self.screen, self.controller, self.storage)
        }
        
        self.state = "MENU"

    def run(self):
        """Loop principal que gere as transições entre o menu e as telas de cadastro/jogo."""
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Atalho universal: ESC sempre retorna ao Menu Principal
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "MENU"

            current_view = self.views.get(self.state)
            
            if self.state == "MENU":
                # O Menu recebe o status do deck para gerir o pop-up de aviso internamente
                # Corrigido para passar has_deck como argumento nomeado para o handle_event
                action = current_view.handle_event(events, has_deck=self.controller.has_deck())
                
                if action == "ABRIR SALA":
                    # A ação 'ABRIR SALA' só é retornada pelo menu se o deck for válido
                    print(f"Sala: {current_view.nome_sala} | Jogadores: {current_view.total_jogadores}")
                    # self.state = "SALA_ESPERA" (Implementação futura)
                    
                elif action == "CADASTRAR" or action == "LISTAR DECK":
                    self.state = "CADASTRAR"
                    
                elif action == "SAIR":
                    self.running = False
                    
            elif current_view:
                # Processa lógica de outras telas (ex: Cadastro) e captura retorno
                res = current_view.handle_events(events)
                if res == "MENU":
                    self.state = "MENU"
                    # Força o controlador a recarregar para validar novos cadastros
                    self.controller.reload_data()

            self.draw()
            self.clock.tick(60)

    def draw(self):
        """Renderiza a interface ativa passando o estado de validade do deck para o menu."""
        self.screen.fill((25, 25, 25))

        if self.state == "MENU":
            # Passa o status real do banco de dados para o MainMenu gerir o Pop-up centralizado
            self.views["MENU"].draw(has_deck=self.controller.has_deck())
        elif self.state in self.views:
            self.views[self.state].draw()

        pygame.display.flip()