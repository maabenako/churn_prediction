from pyspark.ml import Pipeline as SparkPipeline
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql import DataFrame
from pyspark.sql.functions import col


# 🔄 Aplico undersampling se a classe de churn for minoritária
def balancear_classes(df: DataFrame) -> DataFrame:
    print("🔄 Aplicando undersampling para balancear classes...")

    count_churn_0 = df.filter(col("Churn") == 0).count()
    count_churn_1 = df.filter(col("Churn") == 1).count()

    if count_churn_1 == 0:
        raise ValueError("⚠️ Nenhum exemplo com Churn=1 encontrado!")

    ratio = count_churn_1 / count_churn_0

    churn_0_sampled = df.filter(col("Churn") == 0).sample(withReplacement=False, fraction=ratio, seed=42)
    churn_1 = df.filter(col("Churn") == 1)

    df_balanceado = churn_0_sampled.unionByName(churn_1)
    print(f"✅ Dataset balanceado: {df_balanceado.count()} registros")

    return df_balanceado


# 🤖 Aqui é onde faço o treino completo com Spark MLlib
def treinar_modelo(df: DataFrame):
    print("📦 Preparando dados para treino...")

    # Detecto colunas categóricas automaticamente (excluindo ID e label)
    colunas_categoricas = [
        col for col in df.columns
        if df.schema[col].dataType.simpleString() == "string" and col not in ["customerID", "Churn"]
    ]

    # Crio indexadores para essas colunas
    indexers = [
        StringIndexer(inputCol=col, outputCol=f"{col}_idx", handleInvalid="keep")
        for col in colunas_categoricas
    ]

    # Identifico as features numéricas
    features_numericas = [
        col for col in df.columns
        if col not in colunas_categoricas + ["customerID", "Churn"]
    ]

    # Agrupo tudo em um vetor de features
    features_final = features_numericas + [f"{col}_idx" for col in colunas_categoricas]
    assembler = VectorAssembler(inputCols=features_final, outputCol="features")

    # Indexo a variável alvo
    label_indexer = StringIndexer(inputCol="Churn", outputCol="label")

    # Modelo escolhido: Regressão Logística
    lr = LogisticRegression(featuresCol="features", labelCol="label")

    # Montei o pipeline
    pipeline = SparkPipeline(stages=indexers + [assembler, label_indexer, lr])

    print("🎯 Treinando modelo...")
    model = pipeline.fit(df)

    # Aplico o modelo no próprio dataset para avaliar
    predictions = model.transform(df)

    # Chamo a função de ajuste de tipos antes de seguir
    predictions = ajustar_tipos_predicoes(predictions)

    # Avalio a performance com AUC
    evaluator = BinaryClassificationEvaluator(labelCol="label")
    auc = evaluator.evaluate(predictions)
    print(f"✅ AUC: {auc:.4f}")

    return predictions, model


# 🔧 Após o modelo gerar as predições, garanto que prediction e Churn estejam como inteiros
def ajustar_tipos_predicoes(df: DataFrame) -> DataFrame:
    return df.withColumn("prediction", col("prediction").cast("int")) \
             .withColumn("Churn", col("Churn").cast("int"))
