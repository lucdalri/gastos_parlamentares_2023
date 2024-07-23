# %% Importando as bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% Importando os dados
gastos2023 = pd.read_csv('./Data/Ano-2023.csv', delimiter=';')
gastos2023.head()

## Explorando os dados iniciais
# %%
gastos2023.tail()
# %%
gastos2023.info()
# %%
gastos2023.shape
# %%
gastos2023.isna().sum()


# %% Criando dados agregados
gastos2023_parlamentar = gastos2023.groupby(['txNomeParlamentar', 'sgPartido', 'sgUF']).agg({'vlrLiquido' : 'sum'}).reset_index()
gastos2023_parlamentar['txNomeParlamentar'] = gastos2023_parlamentar['txNomeParlamentar'] + ' (' + gastos2023_parlamentar['sgPartido'] + ')'
gastos2023_partido = gastos2023.groupby(['sgPartido']).agg({'vlrLiquido' : 'sum', 'txNomeParlamentar' : 'nunique'}).reset_index()
gastos2023_partido['gastosParlamentar'] = gastos2023_partido['vlrLiquido'] / gastos2023_partido['txNomeParlamentar']
gastos2023_item = gastos2023.groupby(['txtDescricao']).agg({'vlrLiquido' : 'sum'}).sort_values(by='vlrLiquido', ascending=False).reset_index()
gastos2023_item.columns = ['Item', 'Valor Líquido (R$)']
# %% Analisando alguns dados dos parlamentares
gastos2023_parlamentar.describe()
# %%
gastos2023_parlamentar['vlrLiquido'].sum()
# %% Criando um gráfico dos gastos por parlamentares
plt.figure(figsize=(10,8))
grafico_parlamentares = sns.barplot(gastos2023_parlamentar.sort_values(by='vlrLiquido', ascending=False).head(10), 
            x='vlrLiquido', 
            y='txNomeParlamentar',
            hue='vlrLiquido',
            palette='crest',
            legend=False)
grafico_parlamentares.set(xlabel='Gasto Total', ylabel='Parlamentar')
for container in grafico_parlamentares.containers:
    grafico_parlamentares.bar_label(container, fmt=' R$%.2f', fontsize = 12)
plt.title('Gasto total por parlamentar')
sns.despine(ax=grafico_parlamentares, top=True, right=True)

# %% Analisando alguns dados dos partidos
with pd.option_context('display.float_format', '{:.2f}'.format):
    display(gastos2023_partido.describe())

# %% Criando um gráfico dos gastos por partido

plt.figure(figsize=(10,8))
grafico_partido = sns.barplot(gastos2023_partido.sort_values(by='vlrLiquido', ascending=False),
            x='vlrLiquido', 
            y='sgPartido',
            hue='vlrLiquido',
            palette='crest',
            legend=False)
grafico_partido.set(xlabel='Gasto Total', ylabel='Partido')
for container in grafico_partido.containers:
    grafico_partido.bar_label(container, fmt=' R$%.2f', fontsize = 12)
plt.title('Gasto total por partido')
sns.despine(ax=grafico_partido, top=True, right=True)

# %% Criando um gráfico dos gastos do partido por parlamentar
plt.figure(figsize=(10,8))
grafico_partido_parlamentar = sns.barplot(gastos2023_partido.sort_values(by='gastosParlamentar', ascending=False),
            x='gastosParlamentar', 
            y='sgPartido',
            hue='gastosParlamentar',
            palette='crest',
            legend=False)
grafico_partido_parlamentar.set(xlabel='Gasto por Parlamentar', ylabel='Partido')
for container in grafico_partido_parlamentar.containers:
    grafico_partido_parlamentar.bar_label(container, fmt=' R$%.2f', fontsize = 12)
plt.title('Gastos do partido por parlamentar')
sns.despine(ax=grafico_partido_parlamentar, top=True, right=True)

# %%
gastos2023_item