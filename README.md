# 🎮 Análise de Vendas Globais de Games

Este projeto realiza a **análise exploratória** e a **visualização interativa** de dados de vendas globais de jogos de videogame, utilizando **Python** e **Streamlit**.

---

## 📌 Objetivo
O objetivo é identificar padrões de vendas por:
- **Gênero**
- **Ano de lançamento**
- **Região**
- **Publisher**
- **Plataforma**

E apresentar insights em um **dashboard interativo**.

---

## 📂 Estrutura do Projeto

game-sales-analysis/
├── data/ # (Ignorada no GitHub) Contém o vgsales.csv
├── outputs/ # (Ignorada no GitHub) Armazena tabelas e gráficos gerados
├── 01_data_cleaning.py # Limpeza e padronização dos dados
├── 02_eda.py # Análise exploratória (gera tabelas CSV)
├── 03_visualizations.py# Criação de gráficos PNG
├── app.py # Dashboard interativo com Streamlit
├── requirements.txt # Dependências do projeto
├── .gitignore # Arquivos/pastas ignorados pelo Git
└── README.md # Documentação do projeto

---

## 📥 Dataset

Este projeto utiliza o dataset **Video Game Sales** disponível no Kaggle:

🔗 [Baixar no Kaggle](https://www.kaggle.com/datasets/gregorut/videogamesales)

Após o download, salve o arquivo `vgsales.csv` dentro da pasta `data/` na raiz do projeto:

game-sales-analysis/
data/
vgsales.csv

> **Atenção:** A pasta `data/` está no `.gitignore`, então o arquivo não será enviado ao GitHub.

---

## ⚙️ Instalação e Execução

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/joaodrumonte/game-sales-analysis.git
cd game-sales-analysis

2️⃣ Criar ambiente virtual e instalar dependências
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

3️⃣ Rodar os scripts na ordem
# 1) Limpeza e padronização
python 01_data_cleaning.py

# 2) Análise exploratória
python 02_eda.py

# 3) Visualizações
python 03_visualizations.py

# 4) Dashboard Streamlit
streamlit run app.py

📊 Exemplos de Resultados
Vendas Globais por Gênero

Evolução Anual de Vendas

Participação por Região

Correlação entre Vendas

🛠️ Tecnologias Utilizadas

Python (pandas, numpy, matplotlib, seaborn)

Streamlit (dashboard interativo)

Git/GitHub (versionamento e publicação)

👨‍💻 Autor

Desenvolvido por João Carlos Alexandre
🔗 GitHub: joaodrumonte
🔗 LinkedIn: João Carlos Alexandre