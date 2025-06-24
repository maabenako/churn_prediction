# src/churn_analytics/pipelines/eda/pipeline.py
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import resumo_estatistico, distribuicao_churn, verificar_nulos

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=distribuicao_churn,
            inputs="telco_churn_intermediate",
            outputs=None,
            name="distribuicao_churn_node",
        ),
        node(
            func=resumo_estatistico,
            inputs="telco_churn_intermediate",
            outputs=None,
            name="resumo_estatistico_node",
        ),
        node(
            func=verificar_nulos,
            inputs="telco_churn_intermediate",
            outputs="telco_churn_limpo",
            name="verificar_nulos_node",
        ),
    ])
