import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

raw_path = DATA_DIR / "vgsales.csv"
clean_path = DATA_DIR / "vgsales_clean.csv"

if not raw_path.exists():
    raise FileNotFoundError("Não encontrei data/vgsales.csv. Baixe do Kaggle e salve neste caminho.")

print("\n[1/5] Lendo dataset bruto...")
df = pd.read_csv(raw_path)
print("Linhas x Colunas (bruto):", df.shape)

# Normaliza espaços/strings em colunas textuais
for col in ["Name", "Platform", "Genre", "Publisher"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# Converte Year para inteiro nulo (Int64)
print("[2/5] Corrigindo tipos e normalizando campos...")
df["Year"] = pd.to_numeric(df.get("Year"), errors="coerce").round().astype("Int64")

# Padroniza categorias
if "Platform" in df.columns:
    df["Platform"] = df["Platform"].str.upper()
if "Genre" in df.columns:
    df["Genre"] = df["Genre"].str.title()
if "Publisher" in df.columns:
    df["Publisher"] = df["Publisher"].replace({"nan": np.nan}).fillna("Unknown").str.title()

# Remove linhas sem campos críticos
print("[3/5] Removendo linhas inválidas e duplicatas...")
critical_cols = ["Name", "Platform", "Genre", "Global_Sales"]
for c in critical_cols:
    if c not in df.columns:
        raise KeyError(f"Coluna obrigatória ausente no CSV: {c}")

df = df.dropna(subset=["Name", "Platform", "Genre"])  # tolera Year ausente

# Remove duplicatas por jogo+plataforma (mantém a maior venda global)
if {"Name", "Platform", "Global_Sales"}.issubset(df.columns):
    df = df.sort_values("Global_Sales", ascending=False)
    df = df.drop_duplicates(subset=["Name", "Platform"], keep="first")

# Cria a coluna Decade (1990, 2000, ...)
print("[4/5] Criando coluna 'Decade'...")
if "Year" in df.columns:
    decade = (df["Year"].floordiv(10) * 10).astype("Int64")
    df["Decade"] = decade
else:
    df["Decade"] = pd.Series([pd.NA] * len(df), dtype="Int64")

# Ordena colunas de forma amigável
ordered_cols = [
    "Rank", "Name", "Platform", "Year", "Decade", "Genre", "Publisher",
    "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"
]
existing = [c for c in ordered_cols if c in df.columns]
remaining = [c for c in df.columns if c not in existing]
df = df[existing + remaining]

# Salva dataset limpo
print("[5/5] Salvando dataset limpo em data/vgsales_clean.csv...")
df.to_csv(clean_path, index=False)

print("\nConcluído!")
print("Linhas x Colunas (limpo):", df.shape)
print("Registros com Year ausente:", int(df["Year"].isna().sum()))
print("Exemplo de linhas:")
print(df.head(5))