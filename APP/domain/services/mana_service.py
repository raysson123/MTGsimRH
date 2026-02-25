from APP.domain.models.card_model import CardModel
from APP.domain.models.player_model import PlayerModel

class ManaService:
    """
    Serviço Especialista. Isola a lógica de identificação e geração de mana,
    aliviando o MatchController dessa responsabilidade.
    """

    @staticmethod
    def identificar_cor_terreno(card: CardModel) -> str:
        """Lê os dados da carta e descobre a cor da mana que ela gera."""
        nome = card.name.lower()
        
        # 1. Terrenos Básicos
        if "mountain" in nome or "montanha" in nome: return "R"
        if "forest" in nome or "floresta" in nome: return "G"
        if "plains" in nome or "planície" in nome: return "W"
        if "island" in nome or "ilha" in nome: return "U"
        if "swamp" in nome or "pântano" in nome: return "B"
        
        # 2. Dual Lands / Terrenos Especiais (Baseado na Identidade Scryfall)
        if card.color_identity:
            cor = card.color_identity[0].upper()
            if cor in ["W", "U", "B", "R", "G"]:
                return cor
                
        # 3. Fallback (Terrenos que geram apenas incolor)
        return "C"

    @staticmethod
    def tap_land_for_mana(player: PlayerModel, card: CardModel) -> bool:
        """Vira o terreno e adiciona a mana ao jogador de forma segura."""
        # Garante que está no campo e desvirado
        if card not in player.battlefield_lands:
            return False
            
        if card.is_tapped:
            return False
            
        # Executa a ação
        card.tap()
        cor_gerada = ManaService.identificar_cor_terreno(card)
        player.add_mana(cor_gerada, 1)
        
        print(f"[MANA] {player.name} virou '{card.name}' e gerou 1 mana [{cor_gerada}].")
        return True