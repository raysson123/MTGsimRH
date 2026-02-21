
# 🎴 MTG Simulator 

O **MTG Simulator** é um ambiente de simulação para Magic: The Gathering, focado no formato **Commander (EDH)**. Desenvolvido em Python com a biblioteca **Pygame**, o projeto utiliza uma arquitetura **MVC** (Model-View-Controller) rigorosa para garantir alta fidelidade às regras oficiais e performance fluida.

## 👨‍💻 Desenvolvedores

* **HERANDY ALEXSANDER MELO DE BARROS**
* **Raysson**

## 🚀 Como Instalar e Rodar

### 1. Pré-requisitos

* **Python 3.10** ou superior.
* **PIP** (Gerenciador de pacotes do Python).

### 2. Configurar Ambiente Virtual (Recomendado)

```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt

```

**Tecnologias Utilizadas:**

* **Pygame (2.6.1):** Motor gráfico e gerenciamento de inputs.
* **Pydantic (2.12.5):** Modelagem imutável e validação de dados das cartas.
* **Requests:** Integração com a API Scryfall para busca de metadados.
* **Tkinter:** Interface de sistema para seleção de arquivos `.txt`.

### 4. Iniciar o Simulador

```bash
python main.py

```

---

## 📂 Estrutura de Pastas (Arquitetura MVC)

* **`APP/core/`**: Motores principais de renderização (`engine.py`) e controle de telas (`screen_manager.py`).
* **`APP/domain/`**: Lógica pura de Magic. Contém o `MatchModel` (estado global), `PlayerModel` (gavetas de zona) e o `RuleEngine` (o Juiz do jogo).
* **`APP/controllers/`**: O cérebro do projeto. Conecta os dados à interface e orquestra transições de fase e turno.
* **`APP/UI/`**: Componentes visuais modulares (`CardUI`, `ZoneUI`) e layouts dinâmicos baseados em grade.
* **`APP/infrastructure/`**: Serviços de persistência, download de imagens e gestão de cache (`AssetManager`).
* **`data/` & `assets/**`: Repositórios locais de JSONs e imagens (protegidos contra commits pesados via `.gitignore`).

---

## 🚦 Etapa Atual: **Mecânicas de Campo e Estabilidade**

O projeto avançou para a fase de **Simulação de Campo**, onde as cartas não são apenas visualizadas, mas interagem fisicamente com as zonas de jogo.

### ✅ Funcionalidades Prontas:

* **Layout Profissional:** Interface inspirada no MTG Arena, com barra superior de fases fixa e barra inferior de ações para evitar poluição no campo.
* **Sincronização em Tempo Real:** O `GameUIManager` garante que toda alteração na mão ou campo do jogador seja refletida instantaneamente na tela através de cache de memória RAM.
* **Física de D20:** Sistema de rolagem de iniciativa com física pseudo-3D e animações de impacto.
* **Importação Automática:** Lê arquivos `.txt`, baixa artes em alta resolução da Scryfall e estrutura os dados localmente para uso offline.
* **Efeito de Embaralhamento:** Animação dinâmica de cartas voando e sobreposição durante o Shuffle inicial.

### 🛠️ Próximos Passos:

1. **Mecânica de Tap/Untap:** Implementar o giro das cartas (90°) para geração de mana e ataque.
2. **Lógica de Combate:** Declaração formal de atacantes/bloqueadores e cálculo automático de vida.
3. **IA do Oponente:** Inteligência artificial básica para o P2 tomar decisões de descida de terreno e feitiços.

---

**Projeto MTG Simulator** - *Desenvolvido para alta performance e fidelidade às regras do Magic.*

