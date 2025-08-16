# 03_visualizations.py - Versão Simplificada
import pandas as pd
import matplotlib.pyplot as plt

# Configuração segura
plt.style.use('default')

# Gráficos básicos
df = pd.read_csv("data/vgsales_clean.csv")

# Gráfico 1 - Vendas por Gênero
plt.figure(figsize=(8,4))
df['Genre'].value_counts().plot(kind='bar')
plt.savefig("outputs/genre_distribution.png")

# Gráfico 2 - Vendas por Região
plt.figure(figsize=(8,4))
df[['NA_Sales','EU_Sales','JP_Sales']].sum().plot(kind='bar')
plt.savefig("outputs/region_distribution.png")