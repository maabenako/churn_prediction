from pyspark.sql import DataFrame
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 📊 Calcula métricas do modelo para visualização posterior no dashboard
def gerar_metricas_avancadas(df: DataFrame) -> pd.DataFrame:
    df_pandas = df.select("Churn", "prediction").toPandas()

    from sklearn.metrics import classification_report
    relatorio = classification_report(
        df_pandas["Churn"], df_pandas["prediction"], output_dict=True
    )
    resultado = pd.DataFrame(relatorio).transpose().reset_index()
    resultado.rename(columns={"index": "classe"}, inplace=True)
    return resultado

# 📈 Gera gráficos de distribuição, correlação e outliers salvos em arquivos
def gerar_graficos_exploratorios(df: DataFrame):
    df_pandas = df.toPandas()
    pasta_saida = "data/09_visuals/"
    os.makedirs(pasta_saida, exist_ok=True)

    # 🔥 Gráfico 1 - Correlação
    fig1, ax1 = plt.subplots(figsize=(12, 10))
    corr = df_pandas.corr(numeric_only=True)
    sns.heatmap(corr, cmap="coolwarm", annot=True, fmt=".2f", ax=ax1)
    ax1.set_title("Mapa de Correlação")
    plt.tight_layout()

    # 📤 Gráfico 2 - Distribuição de 'MonthlyCharges'
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.histplot(data=df_pandas, x="MonthlyCharges", hue="Churn", kde=True, element="step", ax=ax2)
    ax2.set_title("Distribuição de MonthlyCharges")
    plt.tight_layout()

    # 🧯 Gráfico 3 - Outliers em 'TotalCharges'
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    sns.boxplot(x="Churn", y="TotalCharges", data=df_pandas, ax=ax3)
    ax3.set_title("Boxplot de TotalCharges por Churn")
    plt.tight_layout()

    # 📁 Extra: salvar imagens também no disco
    fig1.savefig(os.path.join(pasta_saida, "mapa_correlacao.png"))
    fig2.savefig(os.path.join(pasta_saida, "distribuicao_MonthlyCharges.png"))
    fig3.savefig(os.path.join(pasta_saida, "boxplot_TotalCharges.png"))
    plt.close("all")

    print("🎨 Gráficos salvos em: data/09_visuals/")

    return fig2, fig1, fig3  # Retorno na ordem dos outputs declarados no pipeline
