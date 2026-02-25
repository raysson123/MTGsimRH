from enum import Enum
from typing import Dict

class ManaType(str, Enum):
    """
    Define estritamente quais são as manas válidas no jogo.
    Evita que o sistema tente adicionar uma mana 'X' ou 'Y' por engano.
    """
    WHITE = "W"
    BLUE = "U"
    BLACK = "B"
    RED = "R"
    GREEN = "G"
    COLORLESS = "C"
    GENERIC = "generic" # Usado apenas para CUSTO, não pode ser gerado.

class ManaPool:
    def __init__(self):
        """
        Representa a reserva de mana de um jogador.
        Guarda a quantidade de cada cor e tem as regras de como gastar.
        """
        self.pool: Dict[str, int] = {
            ManaType.WHITE.value: 0,
            ManaType.BLUE.value: 0,
            ManaType.BLACK.value: 0,
            ManaType.RED.value: 0,
            ManaType.GREEN.value: 0,
            ManaType.COLORLESS.value: 0
        }

    def add_mana(self, mana_type: str, amount: int = 1):
        """Adiciona mana à reserva, garantindo que seja um tipo válido."""
        if mana_type in self.pool:
            self.pool[mana_type] += amount
            return True
        return False

    def clear(self):
        """Esvazia a reserva de mana (Ocorre na virada de fases/turnos)."""
        for color in self.pool:
            self.pool[color] = 0

    def get_total(self) -> int:
        """Retorna o total de mana disponível (soma de todas as cores)."""
        return sum(self.pool.values())

    def can_pay(self, parsed_cost: Dict[str, int]) -> bool:
        """
        Simula o pagamento para saber se o jogador TEM a mana necessária.
        Retorna True se puder pagar, False se faltar mana.
        """
        if not parsed_cost: return True
        
        temp_pool = self.pool.copy()
        
        # 1. Paga os custos coloridos específicos primeiro
        for color, amount in parsed_cost.items():
            if color == ManaType.GENERIC.value: continue
            if temp_pool.get(color, 0) < amount:
                return False
            temp_pool[color] -= amount
            
        # 2. Verifica se sobrou o suficiente para pagar o custo genérico
        generic_needed = parsed_cost.get(ManaType.GENERIC.value, 0)
        total_left = sum(temp_pool.values())
        
        return total_left >= generic_needed

    def pay_mana(self, parsed_cost: Dict[str, int]) -> bool:
        """
        Efetua o pagamento real descontando da reserva do jogador.
        Gasta a mana Incolor primeiro para custos genéricos.
        """
        if not self.can_pay(parsed_cost):
            return False

        # 1. Paga custos coloridos específicos
        for color, amount in parsed_cost.items():
            if color == ManaType.GENERIC.value: continue
            self.pool[color] -= amount
            
        # 2. Paga o custo genérico
        generic_needed = parsed_cost.get(ManaType.GENERIC.value, 0)
        
        # Ordem de prioridade para gastar mana genérica (Incolor primeiro)
        priority_order = ["C", "W", "U", "B", "R", "G"]
        
        for color in priority_order:
            if generic_needed <= 0: break
            available = self.pool[color]
            if available > 0:
                pay = min(available, generic_needed)
                self.pool[color] -= pay
                generic_needed -= pay
                
        return True