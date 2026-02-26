# APP/domain/models/game_state.py

from enum import Enum
from typing import Optional

class Phase(str, Enum):
    """
    Enumeração oficial das fases do jogo.
    O Juiz (RuleEngine) usa isso para não errar a regra.
    """
    INICIAL = "INICIAL"
    PRINCIPAL_1 = "PRINCIPAL 1"
    COMBATE = "COMBATE"
    PRINCIPAL_2 = "PRINCIPAL 2"
    FINAL = "FINAL"

class GameState:
    def __init__(self):
        """
        Gerencia o tempo, as fases e de quem é a vez de jogar.
        Isolado do MatchModel para manter o código limpo (Clean Architecture).
        """
        self.turn_number: int = 1
        self.active_player_id: Optional[str] = None # Quem é o dono do turno
        self.priority_player_id: Optional[str] = None # Quem pode jogar mágicas agora
        
        # FASES OFICIAIS (Agora usando o Enum blindado)
        self.phases = [
            Phase.INICIAL, 
            Phase.PRINCIPAL_1, 
            Phase.COMBATE, 
            Phase.PRINCIPAL_2, 
            Phase.FINAL
        ]
        self.current_phase_index: int = 0
        
        self.is_game_over: bool = False
        self.winner_id: Optional[str] = None

    @property
    def current_phase(self) -> Phase:
        """Retorna o Enum da fase atual para o Juiz avaliar."""
        return self.phases[self.current_phase_index]

    def iniciar_jogo(self, starting_player_id: str):
        """Prepara o relógio para o turno 1."""
        self.active_player_id = starting_player_id
        self.priority_player_id = starting_player_id
        # Força o início na fase Principal 1 (índice 1) do primeiro turno
        self.current_phase_index = 1
        self.turn_number = 1

    def advance_phase(self) -> bool:
        """
        Avança a fase. Retorna True se o turno mudou, False se continuou no mesmo turno.
        """
        if self.is_game_over:
            return False

        self.current_phase_index += 1
        
        # Se passou da última fase ("FINAL"), vira o turno e zera o índice
        if self.current_phase_index >= len(self.phases):
            self.current_phase_index = 0
            self.turn_number += 1
            return True # O turno mudou!
            
        return False