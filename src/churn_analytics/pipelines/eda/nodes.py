# src/churn_analytics/pipelines/eda/nodes.py
from pyspark.sql import DataFrame, functions as F

def resumo_estatistico(df: DataFrame) -> None:
    print("📊 Resumo estatístico:")
    df.describe().show()

def distribuicao_churn(df: DataFrame) -> None:
    print("📈 Distribuição da variável 'Churn':")
    df.groupBy("Churn").count().show()

def verificar_nulos(df: DataFrame) -> DataFrame:
    print("🎯 Verificando valores nulos:")
    df.select([
        F.count(F.when(F.col(c).isNull(), c)).alias(c)
        for c in df.columns
    ]).show()

    media_total = df.select(F.mean("TotalCharges")).first()[0]
    print(f"📥 Preenchendo nulos de 'TotalCharges' com a média: {media_total:.2f}")

    df_corrigido = df.withColumn(
        "TotalCharges",
        F.when(F.col("TotalCharges").isNull(), media_total).otherwise(F.col("TotalCharges"))
    )

    return df_corrigido
