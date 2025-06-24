from kedro.pipeline import Pipeline, node, pipeline
from .nodes import avaliar_modelo

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=avaliar_modelo,
            inputs="predictions",
            outputs="avaliacao_modelo",
            name="avaliar_modelo_node",
        ),
    ])
