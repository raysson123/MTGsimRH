from APP.domain.models.card_model import CardModel
from APP.domain.models.deck_model import DeckModel

class DeckBuilderService:
    """
    Serviço de Domínio responsável por ler o dicionário bruto (JSON)
    e fabricar as instâncias vivas (Objetos) das cartas e do baralho.
    """

    @staticmethod
    def build_from_json(deck_data: dict) -> DeckModel:
        """
        Recebe os dados brutos do DeckRepository, cria os objetos Pydantic
        e devolve um DeckModel pronto para o combate.
        """
        deck = DeckModel()
        deck.name = deck_data.get("name", "Sem Nome")
        commander_name = deck_data.get("commander", "")
        
        cartas_brutas = deck_data.get("cards", [])

        for raw_card in cartas_brutas:
            qtd = raw_card.get("quantity", 1)
            
            # --- MAPEAMENTO ATUALIZADO ---
            # Agora ele puxa TODOS os campos que você tem no seu JSON oficial
            card_args = {
                "name": raw_card.get("name", "Desconhecido"),
                "printed_name": raw_card.get("printed_name", ""),
                "type_line": raw_card.get("type_line", ""),
                "categoria": raw_card.get("categoria", ""),
                "mana_cost": raw_card.get("mana_cost", ""),
                "cmc": float(raw_card.get("cmc") or 0.0), 
                "colors": raw_card.get("colors", []),
                "color_identity": raw_card.get("color_identity", []),
                "image_url": raw_card.get("image_url", ""),
                "oracle_text": raw_card.get("oracle_text", ""),
                "rarity": raw_card.get("rarity", ""),
                
                # Pega as estatísticas transformando em string com segurança
                "power": str(raw_card.get("power")) if raw_card.get("power") is not None else None,
                "toughness": str(raw_card.get("toughness")) if raw_card.get("toughness") is not None else None,
                "loyalty": str(raw_card.get("loyalty")) if raw_card.get("loyalty") is not None else None,
                
                # Mantém o fallback para a imagem, priorizando o seu "local_image_path"
                "local_image_path": raw_card.get("local_image_path") or raw_card.get("ref_image") or raw_card.get("image_path")
            }

            # Verifica se esta carta é o Comandante do deck
            is_commander = (card_args["name"] == commander_name)

            if is_commander and qtd > 0:
                # Copia os argumentos, avisa o Model que é o comandante e instancia
                cmd_args = card_args.copy()
                cmd_args["is_commander"] = True
                
                deck.commander_card = CardModel(**cmd_args)
                qtd -= 1 # Retira 1 cópia que iria para o grimório
                
            # Instancia as cópias físicas da carta para o grimório
            for _ in range(qtd):
                nova_carta = CardModel(**card_args)
                deck.library.append(nova_carta)

        # Atualiza a contagem oficial e embaralha o grimório
        deck.total_cards_initial = len(deck.library) + (1 if getattr(deck, 'commander_card', None) else 0)
        deck.embaralhar()

        return deck