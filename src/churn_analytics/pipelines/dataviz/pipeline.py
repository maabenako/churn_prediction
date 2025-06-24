# src/churn_analytics/pipelines/dataviz/pipeline.py
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import gerar_metricas_avancadas, gerar_graficos_exploratorios

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=gerar_metricas_avancadas,
            inputs="predictions",
            outputs="metricas_avancadas",
            name="gerar_metricas_avancadas_node",
        ),
        node(
            func=gerar_graficos_exploratorios,
            inputs="telco_churn_com_features",
            outputs=[
                "grafico_distribuicao_churn",
                "grafico_correlacao",
                "grafico_outliers"
            ],
            name="gerar_graficos_exploratorios_node",
        ),
    ])
