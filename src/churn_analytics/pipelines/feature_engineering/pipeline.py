from kedro.pipeline import Pipeline, node, pipeline
from .nodes import tratar_outliers, criar_variaveis, aplicar_string_indexers, montar_dataset_features



def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=tratar_outliers,
            inputs="telco_churn_limpo",
            outputs="telco_churn_outliers_tratado",
            name="tratar_outliers_node",
        ),
        node(
            func=criar_variaveis,
            inputs="telco_churn_outliers_tratado",
            outputs="telco_churn_com_variaveis",
            name="criar_variaveis_node",
        ),
        node(
            func=aplicar_string_indexers,
            inputs="telco_churn_com_variaveis",
            outputs="telco_churn_indexado",
            name="aplicar_string_indexers_node",
        ),
        node(
            func=montar_dataset_features,
            inputs="telco_churn_indexado",
            outputs="telco_churn_com_features",
            name="montar_dataset_final_node",
        ),
    ])

