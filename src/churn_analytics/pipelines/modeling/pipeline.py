from kedro.pipeline import Pipeline, node, pipeline
from .nodes import balancear_classes, treinar_modelo, ajustar_tipos_predicoes

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=balancear_classes,
            inputs="telco_churn_com_features",
            outputs="dados_balanceados",
            name="balancear_classes_node",
        ),
        node(
            func=treinar_modelo,
            inputs="dados_balanceados",
            outputs=["predictions_raw", "modelo_logistico_spark"],
            name="treinar_modelo_node",
        ),
        node(
            func=ajustar_tipos_predicoes,
            inputs="predictions_raw",
            outputs="predictions",
            name="ajustar_tipos_predicoes_node",
        ),
    ])
