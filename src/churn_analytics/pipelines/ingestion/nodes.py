from churn_analytics.spark_session import spark
from pyspark.sql import DataFrame

from pyspark.sql import DataFrame

def carregar_telco_dados(df: DataFrame) -> DataFrame:
    print("📊 Esquema dos dados:")
    df.printSchema()

    print("🔍 Amostra dos dados:")
    df.show(10)

    print("🧼 Valores distintos em 'Churn':")
    df.select("Churn").distinct().show()

    return df


