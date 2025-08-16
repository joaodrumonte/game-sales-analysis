import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configurações iniciais
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")

# Configuração do tema dos gráficos
try:
    plt.style.use('seaborn-v0_8')  # Estilo moderno
except:
    plt.style.use('ggplot')  # Fallback

# Configuração da página
st.set_page_config(page_title="Análise de Vendas de Games", layout="wide")

# CSS personalizado
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* Estilos gerais */
    body {
        background-color: #0E1117;
        color: white;
    }
    
    /* Estilos dos tabs */
    .stTabs [role="tablist"] button div div p {
        font-weight: bold;
        color: #4f8bf9;
    }
    .stTabs [aria-selected="true"] div div p {
        color: white !important;
    }
    
    /* Gráficos mais compactos */
    .stPlot {
        margin-top: -1rem;
        border-radius: 8px;
        background-color: #0E1117 !important;
    }
    
    /* Espaçamento melhorado */
    .stMarkdown h3 {
        margin-top: 1.5rem;
        color: white;
    }
    
    /* Reduzir espaçamento entre gráficos */
    .element-container {
        margin-bottom: -1rem;
    }
    
    /* Cores dos textos */
    .st-emotion-cache-1qg05tj {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Configuração do tema do Seaborn
sns.set_theme(
    context='notebook',
    style='darkgrid',
    palette='husl',
    rc={
        'axes.facecolor': '#0E1117',
        'figure.facecolor': '#0E1117',
        'text.color': 'white',
        'axes.labelcolor': 'white',
        'xtick.color': 'white',
        'ytick.color': 'white'
    }
)

# Título
st.title("📊 Análise de Vendas Globais de Games")

# Carregar dados
@st.cache_data
def load_data():
    clean_path = DATA_DIR / "vgsales_clean.csv"
    if not clean_path.exists():
        st.error("Execute primeiro 01_data_cleaning.py")
        return None
    return pd.read_csv(clean_path, dtype={"Year": "Int64", "Decade": "Int64"})

df = load_data()

if df is not None:
    # Sidebar com filtros
    with st.sidebar:
        st.header("🔍 Filtros")
        
        # Filtro por década
        decades = sorted(df['Decade'].dropna().unique())
        selected_decades = st.multiselect(
            "Décadas:",
            options=decades,
            default=[]
        )
        
        # Filtro por plataforma
        platforms = sorted(df['Platform'].unique())
        selected_platforms = st.multiselect(
            "Plataformas:",
            options=platforms,
            default=[]
        )
        
        # Filtro por gênero
        genres = sorted(df['Genre'].unique())
        selected_genres = st.multiselect(
            "Gêneros:",
            options=genres,
            default=[]
        )

    # Aplicar filtros
    filtered_df = df.copy()
    if selected_decades:
        filtered_df = filtered_df[filtered_df['Decade'].isin(selected_decades)]
    if selected_platforms:
        filtered_df = filtered_df[filtered_df['Platform'].isin(selected_platforms)]
    if selected_genres:
        filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genres)]

    # Métricas
    st.header("📈 Métricas Gerais")
    cols = st.columns(4)
    cols[0].metric("Total de Jogos", len(filtered_df))
    cols[1].metric("Vendas Globais", f"{filtered_df['Global_Sales'].sum():.2f}M")
    cols[2].metric("Vendas NA", f"{filtered_df['NA_Sales'].sum():.2f}M")
    cols[3].metric("Vendas EU", f"{filtered_df['EU_Sales'].sum():.2f}M")

    # Abas principais
    tab1, tab2, tab3 = st.tabs(["📊 Gráficos Compactos", "🎮 Top Jogos", "💾 Dados Completos"])

    with tab1:
        # Primeira linha de gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 Gêneros por Vendas")
            fig1, ax1 = plt.subplots(figsize=(6, 3.5), facecolor='#0E1117')
            genre_sales = filtered_df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False).head(10)
            sns.barplot(
                x=genre_sales.values,
                y=genre_sales.index,
                palette="husl"
            )
            plt.xlabel("Vendas (milhões)", color='white')
            plt.ylabel("Gênero", color='white')
            ax1.tick_params(colors='white')
            ax1.spines['bottom'].set_color('white')
            ax1.spines['left'].set_color('white')
            plt.tight_layout()
            st.pyplot(fig1)
        
        with col2:
            st.subheader("Top 10 Plataformas")
            fig2, ax2 = plt.subplots(figsize=(6, 3.5), facecolor='#0E1117')
            platform_sales = filtered_df.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False).head(10)
            sns.barplot(
                x=platform_sales.values,
                y=platform_sales.index,
                palette="husl"
            )
            plt.xlabel("Vendas (milhões)", color='white')
            plt.ylabel("Plataforma", color='white')
            ax2.tick_params(colors='white')
            ax2.spines['bottom'].set_color('white')
            ax2.spines['left'].set_color('white')
            plt.tight_layout()
            st.pyplot(fig2)
        
        # Segunda linha de gráficos
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Evolução Anual das Vendas")
            fig3, ax3 = plt.subplots(figsize=(6, 3.5), facecolor='#0E1117')
            annual_sales = filtered_df.dropna(subset=["Year"]).groupby("Year")["Global_Sales"].sum().reset_index()
            sns.lineplot(
                data=annual_sales,
                x="Year",
                y="Global_Sales",
                marker="o",
                color="#4f8bf9"
            )
            plt.xlabel("Ano", color='white')
            plt.ylabel("Vendas (milhões)", color='white')
            ax3.tick_params(colors='white')
            ax3.spines['bottom'].set_color('white')
            ax3.spines['left'].set_color('white')
            plt.tight_layout()
            st.pyplot(fig3)
        
        with col4:
            st.subheader("Vendas por Região")
            fig4, ax4 = plt.subplots(figsize=(6, 3.5), facecolor='#0E1117')
            region_sales = filtered_df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum().reset_index()
            region_sales.columns = ['Região', 'Vendas']
            region_sales['Região'] = region_sales['Região'].str.replace('_Sales', '')
            sns.barplot(
                data=region_sales,
                x='Região',
                y='Vendas',
                palette="husl"
            )
            plt.xlabel("Região", color='white')
            plt.ylabel("Vendas (milhões)", color='white')
            ax4.tick_params(colors='white')
            ax4.spines['bottom'].set_color('white')
            ax4.spines['left'].set_color('white')
            plt.tight_layout()
            st.pyplot(fig4)

    with tab2:
        st.subheader("Top Jogos")
        n_jogos = st.slider("Quantidade de jogos:", 5, 50, 10)
        top_games = filtered_df.sort_values("Global_Sales", ascending=False).head(n_jogos)
        st.dataframe(
            top_games[['Name', 'Platform', 'Year', 'Genre', 'Global_Sales']],
            height=500,
            column_config={
                "Global_Sales": st.column_config.NumberColumn(format="%.2fM")
            }
        )

    with tab3:
        st.subheader("Dados Completos")
        st.dataframe(
            filtered_df,
            height=600,
            column_config={
                "Global_Sales": st.column_config.NumberColumn(format="%.2fM"),
                "NA_Sales": st.column_config.NumberColumn(format="%.2fM"),
                "EU_Sales": st.column_config.NumberColumn(format="%.2fM")
            }
        )
        st.download_button(
            "Exportar CSV",
            data=filtered_df.to_csv(index=False),
            file_name="vgsales_filtered.csv"
        )

else:
    st.error("Dados não encontrados. Verifique o arquivo data/vgsales_clean.csv")