# app.py - Dashboard Streamlit com Font Awesome nos Tabs (Versão Corrigida)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configurações iniciais
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")

# Configuração da página do Streamlit
st.set_page_config(page_title="Análise de Vendas de Games", layout="wide")

# Adicionar CSS do Font Awesome e estilos personalizados
st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* Estilo para substituir os labels dos tabs */
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 0;
        }
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p:before {
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            font-size: 1rem;
        }
        /* Ícones específicos para cada tab */
        .stTabs [data-baseweb="tab-list"] button:nth-child(1) [data-testid="stMarkdownContainer"] p:before {
            content: "\\f201";
            margin-right: 8px;
        }
        .stTabs [data-baseweb="tab-list"] button:nth-child(1) [data-testid="stMarkdownContainer"] p:after {
            content: "Principais Gráficos";
            font-family: sans-serif;
            font-size: 1rem;
        }
        .stTabs [data-baseweb="tab-list"] button:nth-child(2) [data-testid="stMarkdownContainer"] p:before {
            content: "\\f091";
            margin-right: 8px;
        }
        .stTabs [data-baseweb="tab-list"] button:nth-child(2) [data-testid="stMarkdownContainer"] p:after {
            content: "Top Jogos";
            font-family: sans-serif;
            font-size: 1rem;
        }
        .stTabs [data-baseweb="tab-list"] button:nth-child(3) [data-testid="stMarkdownContainer"] p:before {
            content: "\\f108";
            margin-right: 8px;
        }
        .stTabs [data-baseweb="tab-list"] button:nth-child(3) [data-testid="stMarkdownContainer"] p:after {
            content: "Por Plataforma";
            font-family: sans-serif;
            font-size: 1rem;
        }
        .stTabs [data-baseweb="tab-list"] button:nth-child(4) [data-testid="stMarkdownContainer"] p:before {
            content: "\\f1c0";
            margin-right: 8px;
        }
        .stTabs [data-baseweb="tab-list"] button:nth-child(4) [data-testid="stMarkdownContainer"] p:after {
            content: "Dados Completos";
            font-family: sans-serif;
            font-size: 1rem;
        }
        /* Estilos gerais */
        .icon { margin-right: 8px; }
        .metric-icon { font-size: 1.5em; vertical-align: middle; margin-right: 8px; }
        .st-emotion-cache-16txtl3 {padding: 2rem 1rem;}
        .download-icon { font-size: 1.5em; margin-top: 0.7em; }
    </style>
    """,
    unsafe_allow_html=True
)

# Título do dashboard
st.markdown("""
<h1><i class="fas fa-gamepad icon"></i> Análise de Vendas Globais de Video Games</h1>
<p>Dashboard interativo para explorar as vendas de jogos desde 1980 até 2020.<br>
Dados do <a href="https://www.kaggle.com/datasets/gregorut/videogamesales">Kaggle Video Game Sales</a>.</p>
""", unsafe_allow_html=True)

# Carregar dados limpos
@st.cache_data
def load_data():
    clean_path = DATA_DIR / "vgsales_clean.csv"
    if not clean_path.exists():
        st.error("Arquivo de dados limpos não encontrado. Execute primeiro 01_data_cleaning.py")
        return None
    return pd.read_csv(clean_path, dtype={"Year": "Int64", "Decade": "Int64"})

df = load_data()

if df is not None:
    # Sidebar com filtros
    st.sidebar.markdown("<h3><i class='fas fa-filter icon'></i> Filtros</h3>", unsafe_allow_html=True)
    
    # Filtro por década
    decades = sorted(df['Decade'].dropna().unique())
    selected_decades = st.sidebar.multiselect(
        "Selecione as décadas:",
        options=decades,
        default=decades
    )
    
    # Filtro por plataforma
    platforms = sorted(df['Platform'].unique())
    selected_platforms = st.sidebar.multiselect(
        "Selecione as plataformas:",
        options=platforms,
        default=platforms,
    )
    
    # Filtro por gênero
    genres = sorted(df['Genre'].unique())
    selected_genres = st.sidebar.multiselect(
        "Selecione os gêneros:",
        options=genres,
        default=genres,
    )
    
    # Aplicar filtros
    filtered_df = df[
        (df['Decade'].isin(selected_decades)) & 
        (df['Platform'].isin(selected_platforms)) & 
        (df['Genre'].isin(selected_genres))
    ]
    
    # Métricas gerais
    st.markdown("<h3><i class='fas fa-chart-bar icon'></i> Métricas Gerais</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    col1.markdown("""
    <div style='font-size: 1.2em;'>
        <i class="fas fa-gamepad metric-icon"></i> Total de Jogos<br>
        <span style='font-size: 1.5em; font-weight: bold;'>{}</span>
    </div>
    """.format(len(filtered_df)), unsafe_allow_html=True)
    
    col2.markdown("""
    <div style='font-size: 1.2em;'>
        <i class="fas fa-globe-americas metric-icon"></i> Vendas Globais (MM)<br>
        <span style='font-size: 1.5em; font-weight: bold;'>{:.2f}</span>
    </div>
    """.format(filtered_df['Global_Sales'].sum()), unsafe_allow_html=True)
    
    col3.markdown("""
    <div style='font-size: 1.2em;'>
        <i class="fas fa-flag-usa metric-icon"></i> Vendas NA (MM)<br>
        <span style='font-size: 1.5em; font-weight: bold;'>{:.2f}</span>
    </div>
    """.format(filtered_df['NA_Sales'].sum()), unsafe_allow_html=True)
    
    col4.markdown("""
    <div style='font-size: 1.2em;'>
        <i class="fas fa-flag-eu metric-icon"></i> Vendas EU (MM)<br>
        <span style='font-size: 1.5em; font-weight: bold;'>{:.2f}</span>
    </div>
    """.format(filtered_df['EU_Sales'].sum()), unsafe_allow_html=True)
    
    # Abas com Font Awesome - os labels são placeholders que serão substituídos pelo CSS
    tab1, tab2, tab3, tab4 = st.tabs([
        "Principais Gráficos", 
        "Top Jogos", 
        "Por Plataforma", 
        "Dados Completos"
    ])
    
    with tab1:
        st.markdown("<h3><i class='fas fa-chart-line icon'></i> Principais Visualizações</h3>", unsafe_allow_html=True)
        
        # Gráfico 1: Vendas por gênero
        st.markdown("<h4><i class='fas fa-chart-bar icon'></i> Vendas Globais por Gênero</h4>", unsafe_allow_html=True)
        genre_sales = filtered_df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        sns.barplot(x=genre_sales.index, y=genre_sales.values, ax=ax1)
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("Vendas (milhões)")
        st.pyplot(fig1)
        
        # Gráfico 2: Evolução anual
        st.markdown("<h4><i class='fas fa-chart-line icon'></i> Evolução Anual das Vendas Globais</h4>", unsafe_allow_html=True)
        annual_sales = filtered_df.dropna(subset=["Year"]).groupby("Year")["Global_Sales"].sum().reset_index()
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=annual_sales, x="Year", y="Global_Sales", marker="o", ax=ax2)
        st.pyplot(fig2)
        
    with tab2:
        st.markdown("<h3><i class='fas fa-trophy icon'></i> Top Jogos por Vendas Globais</h3>", unsafe_allow_html=True)
        top_n = st.slider("<i class='fas fa-sliders-h icon'></i> Selecione quantos jogos mostrar:", 5, 50, 10)
        top_games = filtered_df.sort_values("Global_Sales", ascending=False).head(top_n)
        st.dataframe(top_games[['Name', 'Platform', 'Year', 'Genre', 'Publisher', 'Global_Sales']])
        
    with tab3:
        st.markdown("<h3><i class='fas fa-desktop icon'></i> Análise por Plataforma</h3>", unsafe_allow_html=True)
        
        # Vendas por plataforma
        st.markdown("<h4><i class='fas fa-chart-bar icon'></i> Vendas por Plataforma</h4>", unsafe_allow_html=True)
        platform_sales = filtered_df.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False)
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        sns.barplot(x=platform_sales.index, y=platform_sales.values, ax=ax3)
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("Vendas Globais (milhões)")
        st.pyplot(fig3)
        
        # Distribuição por plataforma e década
        st.markdown("<h4><i class='fas fa-layer-group icon'></i> Vendas por Plataforma e Década</h4>", unsafe_allow_html=True)
        platform_decade = filtered_df.dropna(subset=["Decade"]).groupby(["Decade", "Platform"])['Global_Sales'].sum().reset_index()
        pivot_data = platform_decade.pivot(index="Platform", columns="Decade", values="Global_Sales")
        fig4, ax4 = plt.subplots(figsize=(12, 8))
        sns.heatmap(pivot_data.fillna(0), annot=True, fmt=".1f", cmap="YlGnBu", ax=ax4)
        st.pyplot(fig4)
        
    with tab4:
        st.markdown("<h3><i class='fas fa-database icon'></i> Dados Completos</h3>", unsafe_allow_html=True)
        st.dataframe(filtered_df)
        
        # Botão de download corrigido (solução para o erro)
        download_col1, download_col2 = st.columns([1, 10])
        with download_col1:
            st.markdown("<div class='download-icon'><i class='fas fa-download'></i></div>", unsafe_allow_html=True)
        with download_col2:
            st.download_button(
                label="Baixar dados filtrados como CSV",
                data=filtered_df.to_csv(index=False).encode('utf-8'),
                file_name='filtered_video_game_sales.csv',
                mime='text/csv'
            )
        
    # Seção de análises pré-calculadas
    st.sidebar.markdown("<h3><i class='fas fa-chart-pie icon'></i> Análises Pré-calculadas</h3>", unsafe_allow_html=True)
    if st.sidebar.button("<i class='fas fa-sync-alt icon'></i> Carregar Análises do EDA", help="Carrega análises geradas pelo script 02_eda.py"):
        try:
            # Carregar análises do EDA
            top10_games = pd.read_csv(OUTPUT_DIR / "top10_games_global.csv")
            genre_sales = pd.read_csv(OUTPUT_DIR / "genre_sales_by_region.csv")
            annual_sales = pd.read_csv(OUTPUT_DIR / "annual_global_sales.csv")
            platform_decade = pd.read_csv(OUTPUT_DIR / "platform_sales_by_decade.csv")
            top_publishers = pd.read_csv(OUTPUT_DIR / "top_publishers_global.csv")
            
            st.markdown("<h3><i class='fas fa-trophy icon'></i> Top 10 Jogos Globais (Pré-calculado)</h3>", unsafe_allow_html=True)
            st.dataframe(top10_games)
            
            st.markdown("<h3><i class='fas fa-building icon'></i> Top Publishers Globais</h3>", unsafe_allow_html=True)
            st.dataframe(top_publishers)
            
        except FileNotFoundError:
            st.error("Arquivos de análise não encontrados. Execute primeiro 02_eda.py")
    
    # Mostrar gráficos pré-renderizados
    if st.sidebar.checkbox("<i class='fas fa-image icon'></i> Mostrar gráficos pré-renderizados", False):
        try:
            st.markdown("<h3><i class='fas fa-image icon'></i> Gráficos Pré-renderizados</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.image(str(OUTPUT_DIR / "plot_genre_global_sales.png"), caption="Vendas Globais por Gênero")
                st.image(str(OUTPUT_DIR / "plot_annual_global_sales.png"), caption="Evolução Anual das Vendas")
            
            with col2:
                st.image(str(OUTPUT_DIR / "plot_region_share_pie.png"), caption="Participação por Região")
                st.image(str(OUTPUT_DIR / "plot_sales_correlation_heatmap.png"), caption="Correlação entre Regiões")
        except FileNotFoundError:
            st.error("Gráficos não encontrados. Execute primeiro 03_visualizations.py")

else:
    st.error("Não foi possível carregar os dados. Verifique se o arquivo data/vgsales_clean.csv existe.")