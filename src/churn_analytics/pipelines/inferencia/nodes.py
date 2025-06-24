from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import pandas as pd

# ✨ Avaliação completa do modelo com verificação de nulos, métricas e salvamento
def avaliar_modelo(predictions: DataFrame) -> pd.DataFrame:
    print("📊 Avaliando modelo de churn...")

    # 🚫 Desabilita o Arrow temporariamente para evitar bugs no toPandas()
    predictions.sparkSession.conf.set("spark.sql.execution.arrow.pyspark.enabled", "false")

    # 🧼 Seleciona só as colunas importantes
    predictions_clean = predictions.select("Churn", "prediction")

    # 📉 Conta quantos dados estão comprometidos por nulos
    total = predictions_clean.count()
    predictions_clean = predictions_clean.dropna(subset=["Churn", "prediction"])
    validos = predictions_clean.count()
    invalidos = total - validos
    perc = 100 * invalidos / total if total > 0 else 0

    print(f"\n🔍 Valores únicos em 'Churn': {predictions_clean.select('Churn').distinct().rdd.flatMap(lambda x: x).collect()}")
    print(f"🔍 Valores únicos em 'prediction': {predictions_clean.select('prediction').distinct().rdd.flatMap(lambda x: x).collect()}")
    print(f"⚠️ Registros totais: {total}")
    print(f"✅ Registros válidos: {validos}")
    print(f"❌ Registros inválidos: {invalidos} ({perc:.2f}%)\n")

    # 📊 Cria DataFrame para matriz de confusão
    cm_df = predictions_clean.groupBy("Churn", "prediction").count().toPandas()

    # ✅ Reativa o Arrow
    predictions.sparkSession.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

    # 🧼 Converte com segurança os tipos para inteiros
    cm_df["Churn"] = cm_df["Churn"].astype(int)
    cm_df["prediction"] = cm_df["prediction"].astype(int)
    cm_df["count"] = cm_df["count"].astype(int)

    # 🔢 Extrai os valores da matriz de confusão
    tp = cm_df.query("Churn == 1 and prediction == 1")["count"].sum()
    tn = cm_df.query("Churn == 0 and prediction == 0")["count"].sum()
    fp = cm_df.query("Churn == 0 and prediction == 1")["count"].sum()
    fn = cm_df.query("Churn == 1 and prediction == 0")["count"].sum()

    # 📈 Métricas ponderadas (seguras e justas)
    y_true = cm_df["Churn"]
    y_pred = cm_df["prediction"]
    weights = cm_df["count"]

    precision = precision_score(y_true, y_pred, sample_weight=weights)
    recall = recall_score(y_true, y_pred, sample_weight=weights)
    f1 = f1_score(y_true, y_pred, sample_weight=weights)
    cm = confusion_matrix(y_true, y_pred, sample_weight=weights)

    # 🧠 Avalia a AUC com Spark
    evaluator = BinaryClassificationEvaluator(
        labelCol="Churn",
        rawPredictionCol="rawPrediction",
        metricName="areaUnderROC"
    )
    auc = evaluator.evaluate(predictions)

    # 📢 Exibe tudo com carinho
    print("✅ Avaliação do Modelo:")
    print(f"AUC: {auc:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("\n📉 Matriz de Confusão:")
    print(cm)

    # 📄 Retorna um Pandas bonitinho para salvar no CSV
    resultado = pd.DataFrame({
        "metric": ["AUC", "Precision", "Recall", "F1", "Churn Previsto (0)", "Churn Previsto (1)"],
        "value": [float(auc), precision, recall, f1, int(tn + fn), int(tp + fp)]
    })

    return resultado

