

# 🎴  MTG Simulator

O **Machete** é um simulador de Magic: The Gathering (MTG) focado no formato Commander, desenvolvido em Python com a biblioteca Pygame. O projeto utiliza uma arquitetura MVC (Model-View-Controller) para garantir uma separação clara entre as regras de jogo, o gerenciamento de dados e a interface visual.

## 👨‍💻 Desenvolvedores

* **HERANDY ALEXSANDER MELO DE BARROS**
* **Raysson (Machete)**

## 🚀 Como Instalar e Rodar

### 1. Pré-requisitos

Certifique-se de ter o **Python 3.10 ou superior** instalado em sua máquina.

### 2. Configurar Ambiente Virtual (Recomendado)

```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

```

### 3. Instalar Dependências

O projeto utiliza bibliotecas específicas para performance e validação de dados. Instale-as utilizando o arquivo fornecido:

```bash
pip install -r requirements.txt

```

**Principais Tecnologias:**

* **Pygame (2.6.1):** Motor gráfico e gerenciamento de eventos.
* **Pydantic (2.12.5):** Modelagem e validação de dados das cartas.
* **Requests:** Integração com a API Scryfall.

### 4. Iniciar o Simulador

```bash
python main.py

```

---

## 📂 Estrutura de Pastas (Hierarquia Correta)

* **`APP/core/`:** Motores principais (`engine.py`) e gerenciador de telas (`screen_manager.py`).
* **`APP/domain/`:** Lógica de negócio, incluindo `CardModel`, `MatchModel` e o motor de regras `RuleEngine`.
* **`APP/infrastructure/`:** Serviços externos (Scryfall) e gestão de mídia (`AssetManager`).
* **`APP/UI/`:** Componentes visuais (`CardUI`, `ZoneUI`) e telas do jogo.
* **`data/`:** Armazenamento de perfis e decks em JSON (protegido pelo `.gitignore`).
* **`assets/`:** Armazenamento das artes das cartas (protegido pelo `.gitignore`).

---

## 🚦 Etapa Atual do Projeto: **Estabilidade e Integração Visual**

O projeto concluiu a fase de **Fiação de Dados**, onde a interface visual foi conectada com sucesso aos modelos de dados reais.

### ✅ O que já está funcionando:

* **Gestão de Assets Direta:** O `AssetManager` carrega imagens usando o caminho exato salvo no JSON (`local_image_path`), eliminando erros de "Imagem não encontrada".
* **Sincronização de Mesa:** A `MatchView` utiliza o `GameUIManager` para manter as cartas sincronizadas entre a lógica do jogo e o que é exibido na tela.
* **Sistema de Registro:** Importação de decks via `.txt` com download automático de artes e estruturação de dados offline.
* **Motor de Regras Inicial:** Validação de descida de terrenos e custos de mana básicos.

### 🛠️ Próximos Passos (Próxima Etapa):

1. **Mecânica de Mana Ativa:** Implementar o clique nos terrenos para "virar" (Tap) e adicionar mana à reserva do jogador.
2. **Lógica de Combate:** Fase de declaração de atacantes e cálculo de dano.
3. **Inteligência Artificial (Bot):** Comportamento automatizado para o Oponente 1 (P2).

---

**Projeto MTG** - *Desenvolvido para alta performance e fidelidade às regras do Magic.*