import streamlit as st
import pandas as pd
import plotly.express as px
#---------------------------------------------------------------------------------
#mudar a cor do fundo para verde claro
st.markdown("""
<style>
.stApp {
    background-color: #E8F5E9;
}
</style>
""", unsafe_allow_html=True)

#para a barra lateral ficar colorida também
st.markdown("""
<style>
.stApp {
    background-color: #E8F5E9;
}

[data-testid="stSidebar"] {
    background-color: #A5D6A7;
}
</style>
""", unsafe_allow_html=True)

#-----------------------------------------------------------------------------------
# Melhoria para o dashboard ocupar toda a largura da tela
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)
#------------------------------------------------------------------------------------
# para inserir a minha imagem no topo

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(
        "Gemini_Generated_Image_ylki4tylki4tylki.png",
        width=300
    )
#-----------------------------------------------------------------------------------


dados = pd.read_excel("Vendas_Base_de_Dados.xlsx")

st.title("Dashboard de Vendas da Sabrina")
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

#---------------------------------------------------------------------------------
# inserção do Top5 de lojas que mais venderam

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


# Inserir filtro de produto mais vendido por quantidade
tipo_analise = st.sidebar.selectbox(
    "Análise de produto:",
    ["Mais vendido por quantidade", "Maior faturamento"]
)


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

#-------------------------------------------------------------------------------------
# gráfico de faturamento por produto

faturamento_produto = (
    dados_filtrados.groupby("Produto")["Faturamento"]
    .sum()
    .reset_index()
    .sort_values("Faturamento", ascending=False)
)

grafico_produto = px.bar(
    faturamento_produto,
    x="Produto",
    y="Faturamento",
    title="Faturamento por produto"
)

st.plotly_chart(grafico_produto)

#---------------------------------------------------------------------------------------
# produto mais vendido

produto_mais_vendido = (
    dados.groupby("Produto")["Quantidade"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

st.subheader("Produto mais vendido")
st.write(produto_mais_vendido.iloc[0])

#-----------------------------------------------------------------------------------
# botões para baixar dados filtrados

csv = dados_filtrados.to_csv(index=False)

st.download_button(
    label="Baixar dados filtrados em CSV",
    data=csv,
    file_name="dados_filtrados.csv",
    mime="text/csv"
)

#----------------------------------------------------------------------------------
# relatório em Markdown para download na barra lateral

relatorio_md = f"""
# Relatório do Dashboard de Vendas

## Resumo geral

- Faturamento total: R$ {faturamento_total:,.2f}
- Total de itens vendidos: {total_itens}
- Número de lojas analisadas: {numero_lojas}

## Filtros aplicados

- Loja selecionada: {loja_escolhida}
- Produto selecionado: {produto_escolhido}

## Top 5 lojas por faturamento

{top5.to_markdown(index=False)}

## Dados filtrados

{dados_filtrados.to_markdown(index=False)}
"""

st.sidebar.download_button(
    label="Baixar relatório em Markdown",
    data=relatorio_md,
    file_name="relatorio_dashboard.md",
    mime="text/markdown"
)
