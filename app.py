import streamlit as st
import pandas as pd
import plotly.express as px

dados = pd.read_excel("Vendas_Base_de_Dados.xlsx")

st.title("Dashboard de Vendas")
st.write("Tabela de vendas do mês:")
st.dataframe(dados)

st.write("Colunas encontradas:")
st.write(list(dados.columns))

dados["Faturamento"] = dados["Quantidade"] * dados["Valor Unitário"]

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