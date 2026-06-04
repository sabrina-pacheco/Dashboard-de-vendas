import streamlit as st
import pandas as pd
import plotly.express as px


# Melhoria para o dasboard ocupar toda a largura da tela
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)



dados = pd.read_excel("Vendas_Base_de_Dados.xlsx")

st.title("Dashboard de Vendas")
st.write("Tabela de vendas do mês:")
st.dataframe(dados)

st.write("Colunas encontradas:")
st.write(list(dados.columns))

dados["Faturamento"] = dados["Quantidade"] * dados["Valor Unitário"]

# adição de indicadores
faturamento_total = dados["Faturamento"].sum()
total_itens = dados["Quantidade"].sum()
numero_lojas = dados["Loja"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}")
col2.metric("Itens Vendidos", total_itens)
col3.metric("Número de Lojas", numero_lojas)
#----------------------------------------------------------------------------


dados_agrupados = (
    dados.groupby("Loja")["Faturamento"]
    .sum()
    .reset_index()
    .sort_values(by="Faturamento", ascending=False)
)

grafico = px.bar(
    dados_agrupados,
    x="Loja",
    y="Faturamento",
    title="Faturamento por Loja"
)

st.plotly_chart(grafico)

top5 = dados_agrupados.head(5)

st.subheader("Top 5 lojas por faturamento")

st.dataframe(top5)

#para inserir filtro para escolher uma loja e ver seus dados

# lojas = sorted(dados['Loja'].unique())
# loja_escolhida = st.sidebar.selectbox('Escolha a loja:', lojas)

# dados_loja = dados[dados['Loja'] == loja_escolhida]
# st.write(f'Dados da loja {loja_escolhida}:')
# st.dataframe(dados_loja)

st.sidebar.header("Filtros")

lojas = sorted(dados["Loja"].unique())
loja_escolhida = st.sidebar.selectbox("Escolha a loja:", lojas)

produtos = ["Todos"] + sorted(dados["Produto"].unique())
produto_escolhido = st.sidebar.selectbox("Escolha o produto:", produtos)

dados_filtrados = dados[dados["Loja"] == loja_escolhida]

if produto_escolhido != "Todos":
    dados_filtrados = dados_filtrados[dados_filtrados["Produto"] == produto_escolhido]

st.write(f"Dados filtrados:")
st.dataframe(dados_filtrados)


# para inserir o gráfico de pizza

grafico_pizza = px.pie(
    dados_agrupados,
    names="Loja",
    values="Faturamento",
    title="Participação das lojas no faturamento"
)

grafico_pizza.update_traces(
    textinfo="percent+label"
)

st.plotly_chart(grafico_pizza)

