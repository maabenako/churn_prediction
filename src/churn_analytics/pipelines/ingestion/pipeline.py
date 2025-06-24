from kedro.pipeline import Pipeline, node
from pyspark.sql import DataFrame  
from .nodes import carregar_telco_dados

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=carregar_telco_dados,
            inputs="telco_churn_raw",
            outputs="telco_churn_intermediate",
            name="carregar_dados_node"
        )
    ])

def processar_dados(df: DataFrame) -> DataFrame:
    # limpeza, transformação, etc
    return df

