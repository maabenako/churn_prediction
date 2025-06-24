from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline

# 🧹 Trata outliers nas colunas numéricas com capping
def tratar_outliers(df: DataFrame) -> DataFrame:
    print("🧹 Tratando outliers com capping...")

    colunas_numericas = ["MonthlyCharges", "TotalCharges", "tenure"]

    for col_nome in colunas_numericas:
        quantiles = df.approxQuantile(col_nome, [0.25, 0.75], 0.05)
        if len(quantiles) < 2:
            continue

        q1, q3 = quantiles
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr

        df = df.withColumn(
            col_nome,
            F.when(F.col(col_nome) < limite_inferior, limite_inferior)
             .when(F.col(col_nome) > limite_superior, limite_superior)
             .otherwise(F.col(col_nome))
        )

    return df

# 🛠️ Cria features binárias úteis
def criar_variaveis(df: DataFrame) -> DataFrame:
    print("🛠️ Criando features novas...")

    df = df.withColumn("PossuiDependente", F.when(F.col("Dependents") == "Yes", 1).otherwise(0)) \
           .withColumn("EhCasado", F.when(F.col("Partner") == "Yes", 1).otherwise(0)) \
           .withColumn("ServicoInternet", F.when(F.col("InternetService") != "No", 1).otherwise(0)) \
           .withColumn("ContratoMensal", F.when(F.col("Contract") == "Month-to-month", 1).otherwise(0)) \
           .withColumn("Churn", F.when(F.col("Churn") == "Yes", 1).otherwise(0))

    return df

# 🏷️ Aplica StringIndexers nas colunas categóricas
def aplicar_string_indexers(df: DataFrame) -> DataFrame:
    print("🏷️ Aplicando StringIndexers...")

    colunas_categoricas = ["gender", "SeniorCitizen", "Partner", "Dependents",
                           "PhoneService", "MultipleLines", "InternetService",
                           "OnlineSecurity", "OnlineBackup", "DeviceProtection",
                           "TechSupport", "StreamingTV", "StreamingMovies",
                           "Contract", "PaperlessBilling", "PaymentMethod"]

    indexers = [
        StringIndexer(inputCol=col, outputCol=f"{col}_index", handleInvalid="keep")
        for col in colunas_categoricas
    ]

    pipeline = Pipeline(stages=indexers)
    model = pipeline.fit(df)
    df_indexado = model.transform(df)

    return df_indexado

# 🧩 Junta todas as colunas finais (exemplo simplificado, ajuste conforme a modelagem)
def montar_dataset_features(df: DataFrame) -> DataFrame:
    print("🧩 Montando dataset final com features...")

    # Aqui você pode selecionar apenas as colunas desejadas
    colunas_finais = [col for col in df.columns if "_index" in col or col in [
        "MonthlyCharges", "TotalCharges", "tenure", "PossuiDependente",
        "EhCasado", "ServicoInternet", "ContratoMensal", "Churn"
    ]]

    return df.select(*colunas_finais)
