from kedro.pipeline import Pipeline
from churn_analytics.pipelines import ingestion, eda, feature_engineering, modeling, inferencia, dataviz


def register_pipelines() -> dict[str, Pipeline]:
    return {
        "__default__": (
            ingestion.create_pipeline()
            + eda.create_pipeline()
            + feature_engineering.create_pipeline()
            + modeling.create_pipeline()
            + inferencia.create_pipeline()
            + dataviz.create_pipeline()
        ),
        "ingestion": ingestion.create_pipeline(),
        "eda": eda.create_pipeline(),
        "feature_engineering": feature_engineering.create_pipeline(),
        "modeling": modeling.create_pipeline(),
        "inferencia": inferencia.create_pipeline(),
        "dataviz": dataviz.create_pipeline(),
    }