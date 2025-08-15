import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set(style="whitegrid")

DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

clean_path = DATA_DIR / "vgsales_clean.csv"
if not clean_path.exists():
    raise FileNotFoundError("Não encontrei data/vgsales_clean.csv. Execute 01_data_cleaning.py primeiro.")

df = pd.read_csv(clean_path, dtype={"Year": "Int64", "Decade": "Int64"})
region_cols = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]

# 1) Barras: vendas globais por gênero
genre_sales = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=genre_sales.index, y=genre_sales.values)
plt.title("Vendas Globais por Gênero")
plt.ylabel("Vendas (milhões)")
plt.xlabel("Gênero")
plt.xticks(rotation=35, ha='right')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "plot_genre_global_sales.png", dpi=150)
plt.close()

# 2) Linha: evolução anual das vendas globais
annual = df.dropna(subset=["Year"]).groupby("Year")["Global_Sales"].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=annual, x="Year", y="Global_Sales", marker="o")
plt.title("Evolução Anual das Vendas Globais")
plt.ylabel("Vendas (milhões)")
plt.xlabel("Ano")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "plot_annual_global_sales.png", dpi=150)
plt.close()

# 3) Pizza: participação por região (total)
region_totals = df[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum()
plt.figure(figsize=(7, 7))
plt.pie(region_totals.values, labels=region_totals.index, autopct='%1.1f%%', startangle=140)
plt.title("Participação por Região (Total Acumulado)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "plot_region_share_pie.png", dpi=150)
plt.close()

# 4) Heatmap: correlação entre regiões e global
plt.figure(figsize=(6, 5))
cor = df[region_cols].corr()
sns.heatmap(cor, annot=True, fmt=".2f", cmap="Blues")
plt.title("Correlação entre Vendas Regionais e Global")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "plot_sales_correlation_heatmap.png", dpi=150)
plt.close()

# 5) Boxplot: distribuição de vendas globais por gênero
plt.figure(figsize=(12, 6))
# Limita a vendas > 0 para boxplot mais legível
subset = df[df["Global_Sales"] > 0]
sns.boxplot(data=subset, x="Genre", y="Global_Sales")
plt.title("Distribuição de Vendas Globais por Gênero")
plt.ylabel("Vendas por Jogo (milhões)")
plt.xlabel("Gênero")
plt.xticks(rotation=35, ha='right')
plt.tight_l