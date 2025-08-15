import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

clean_path = DATA_DIR / "vgsales_clean.csv"
if not clean_path.exists():
    raise FileNotFoundError("Não encontrei data/vgsales_clean.csv. Execute 01_data_cleaning.py primeiro.")

print("\n[EDA] Carregando dataset limpo...")
df = pd.read_csv(clean_path, dtype={"Year": "Int64", "Decade": "Int64"})
print("Linhas x Colunas:", df.shape)

# 1) Top 10 jogos mais vendidos globalmente
print("Gerando Top 10 jogos globais...")
top10_games = df.sort_values("Global_Sales", ascending=False).head(10)
top10_games.to_csv(OUTPUT_DIR / "top10_games_global.csv", index=False)

# 2) Vendas por gênero (mundo e regiões)
print("Agregando vendas por gênero...")
region_cols = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]
genre_sales = df.groupby("Genre")[region_cols].sum().sort_values("Global_Sales", ascending=False)
genre_sales.to_csv(OUTPUT_DIR / "genre_sales_by_region.csv")

# 3) Evolução anual das vendas globais
print("Calculando evolução anual das vendas globais...")
annual_sales = (
    df.dropna(subset=["Year"]).groupby("Year")["Global_Sales"].sum().reset_index()
)
annual_sales.to_csv(OUTPUT_DIR / "annual_global_sales.csv", index=False)

# 4) Plataformas por década
print("Calculando plataformas por década...")
platform_decade = (
    df.dropna(subset=["Decade"]).groupby(["Decade", "Platform"])['Global_Sales']
    .sum().reset_index().sort_values(["Decade", "Global_Sales"], ascending=[True, False])
)
platform_decade.to_csv(OUTPUT_DIR / "platform_sales_by_decade.csv", index=False)

# 5) Publishers mais fortes
print("Calculando publishers com mais vendas globais...")
publisher_rank = df.groupby("Publisher")["Global_Sales"].sum().sort_values(ascending=False).head(20)
publisher_rank = publisher_rank.reset_index().rename(columns={"Global_Sales": "Total_Global_Sales"})
publisher_rank.to_csv(OUTPUT_DIR / "top_publishers_global.csv", index=False)

# 6) Resumo estatístico das colunas de vendas
print("Salvando resumo estatístico...")
df[region_cols].describe().to_csv(OUTPUT_DIR / "sales_describe.csv")

print("\nEDA concluída! Veja os CSVs em ./outputs/")