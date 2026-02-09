import pygame
import threading
from APP.utils.style import GameStyle

class RegisterProgressView:
    def __init__(self, screen, storage, deck_name, file_path):
        """
        Tela de Download com suporte a Threading para não travar o jogo.
        """
        self.screen = screen
        self.storage = storage
        self.deck_name = deck_name
        self.file_path = file_path
        self.fontes = GameStyle.get_fonts()
        
        # Variáveis de Estado Visual
        self.progresso_atual = 0
        self.progresso_total = 0
        self.carta_atual = "Inicializando..."
        self.concluido = False
        self.erro = None
        
        # Controle de Thread
        self.thread_iniciada = False

    def iniciar_fluxo(self, deck_model):
        """
        Chamado pelo ViewManager. Inicia o download em uma thread separada.
        """
        if not self.thread_iniciada:
            # Configura o modelo com o nome (o comandante já foi setado no ViewManager)
            deck_model.name = self.deck_name
            
            # Cria e inicia a thread para não congelar a janela
            t = threading.Thread(target=self._tarefa_download, args=(deck_model,))
            t.daemon = True # Garante que a thread morra se o jogo fechar
            t.start()
            self.thread_iniciada = True

    def _tarefa_download(self, deck_model):
        """
        Lógica pesada que roda em segundo plano.
        """
        try:
            # 1. Ler arquivo
            qtd, linhas = self.storage.analisar_txt(self.file_path)
            self.progresso_total = qtd
            
            # 2. Baixar cartas (atualiza a barra via callback)
            cards = self.storage.processar_download_com_progresso(
                linhas, 
                self._atualizar_progresso
            )
            
            # 3. Atualizar Modelo e Salvar
            deck_model.cards = cards
            self.storage.salvar_deck_inteligente(deck_model)
            
            # Finaliza
            self.concluido = True
            self.carta_atual = "Concluído! Pressione qualquer tecla."
            
        except Exception as e:
            self.erro = str(e)
            self.carta_atual = "Erro no download."

    def _atualizar_progresso(self, atual, total, nome):
        """Callback chamado pelo storage para atualizar a interface."""
        self.progresso_atual = atual
        self.progresso_total = total
        self.carta_atual = nome

    def handle_events(self, events):
        """
        MÉTODO OBRIGATÓRIO (Resolvendo o AttributeError).
        Verifica se acabou e aguarda comando para sair.
        """
        # Se ocorreu erro ou terminou, qualquer tecla volta ao Menu
        if self.concluido or self.erro:
            for event in events:
                if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                    return "MENU"
        
        # Enquanto baixa, não faz nada (bloqueia saída para não corromper)
        return None

    def draw(self):
        """Renderiza a barra de progresso."""
        self.screen.fill(GameStyle.COLOR_BG)
        cx, cy = self.screen.get_rect().center
        
        # Título
        titulo = "BAIXANDO IMAGENS..." if not self.concluido else "CADASTRO FINALIZADO!"
        cor_titulo = GameStyle.COLOR_ACCENT if not self.erro else GameStyle.COLOR_DANGER
        
        txt_t = self.fontes['titulo'].render(titulo, True, cor_titulo)
        self.screen.blit(txt_t, (cx - txt_t.get_width()//2, cy - 100))

        # Se houver erro, exibe e para
        if self.erro:
            msg = self.fontes['status'].render(f"Erro: {self.erro}", True, (255, 100, 100))
            self.screen.blit(msg, (cx - msg.get_width()//2, cy))
            info = self.fontes['label'].render("Pressione qualquer tecla para voltar", True, (150, 150, 150))
            self.screen.blit(info, (cx - info.get_width()//2, cy + 50))
            return

        # Desenha a Barra de Progresso
        largura_barra = 600
        altura_barra = 30
        pos_x = cx - largura_barra // 2
        
        # Fundo da barra
        pygame.draw.rect(self.screen, (40, 40, 40), (pos_x, cy, largura_barra, altura_barra), border_radius=15)
        
        # Preenchimento
        if self.progresso_total > 0:
            pct = self.progresso_atual / self.progresso_total
            largura_fill = int(largura_barra * pct)
            pygame.draw.rect(self.screen, GameStyle.COLOR_ACCENT, (pos_x, cy, largura_fill, altura_barra), border_radius=15)

        # Texto de Status (Carta Atual)
        txt_status = self.fontes['status'].render(f"{self.carta_atual}", True, (200, 200, 200))
        # Limita largura do texto para não sair da tela
        if txt_status.get_width() > 800:
            txt_status = pygame.transform.scale(txt_status, (800, txt_status.get_height()))
            
        self.screen.blit(txt_status, (cx - txt_status.get_width()//2, cy + 50))
        
        # Instrução final
        if self.concluido:
            info = self.fontes['label'].render("Clique para voltar ao Menu", True, (100, 255, 100))
            self.screen.blit(info, (cx - info.get_width()//2, cy + 90))