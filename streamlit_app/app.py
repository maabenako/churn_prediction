import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="📊 Dashboard de Churn", layout="wide")
st.title("📉 Análise de Churn - Telecom")

# Caminhos
pasta_metricas = "/home/maabe/churn_spark/churn_analytics/data/08_reporting"
pasta_graficos = "/home/maabe/churn_spark/churn_analytics/data/09_visuals"

# ================== 🔢 MÉTRICAS ==================
st.header("🔢 Métricas do Modelo")
try:
    metricas_df = pd.read_csv(os.path.join(pasta_metricas, "metricas_avancadas.csv"))
    st.markdown("A tabela abaixo resume as métricas de desempenho do modelo para prever o cancelamento de clientes.")
    st.dataframe(metricas_df, use_container_width=True)
except Exception as e:
    st.warning(f"Erro ao carregar métricas: {e}")

# ================== 🎨 GRÁFICOS EXPLORATÓRIOS ==================
st.header("🎨 Gráficos Exploratórios")

col1, col2 = st.columns(2)

# 🔥 Mapa de correlação
with col1:
    st.subheader("Mapa de Correlação")
    try:
        img_path = os.path.join(pasta_graficos, "grafico_correlacao.png")
        st.image(Image.open(img_path), use_container_width=True)
        st.markdown("🔍 Este mapa mostra o grau de correlação entre as variáveis numéricas. Cores mais intensas representam correlações fortes — positivas ou negativas.")
    except:
        st.warning("Mapa de correlação não encontrado")

# 📊 Distribuição de variáveis
with col2:
    st.subheader("Distribuição de Variáveis")

    # 🧠 Dicionário para nomes legíveis
    distribs = [f for f in os.listdir(pasta_graficos) if f.startswith("grafico_distribuicao_")]
    nomes_legiveis = {arq: arq.replace("grafico_distribuicao_", "").replace(".png", "").capitalize()
                      for arq in distribs}

    if nomes_legiveis:
        escolhido = st.selectbox("Escolha uma variável:", list(nomes_legiveis.values()))
        arq_esc = [k for k, v in nomes_legiveis.items() if v == escolhido][0]
        st.image(Image.open(os.path.join(pasta_graficos, arq_esc)), use_container_width=True)
        st.markdown("📌 Este gráfico mostra como a variável selecionada se distribui entre clientes que **cancelaram** e **não cancelaram**.")
    else:
        st.info("Nenhuma distribuição encontrada.")

# ================== 🧯 BOXPLOTS ==================
st.subheader("🛡️ Boxplots por Churn")
boxplots = [f for f in os.listdir(pasta_graficos) if f.startswith("grafico_outliers")]
if boxplots:
    for bp in boxplots:
        nome_legivel = bp.replace("grafico_outliers_", "").replace(".png", "").capitalize()
        st.image(Image.open(os.path.join(pasta_graficos, bp)), caption=f"Boxplot de {nome_legivel}")
        st.markdown(f"🎁 O boxplot de **{nome_legivel}** permite visualizar outliers e como a variável se comporta entre os grupos com e sem churn.")
else:
    st.info("Nenhum boxplot encontrado.")

