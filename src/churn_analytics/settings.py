"""Project settings. There is no need to edit this file unless you want to change values
from the Kedro defaults. For further information, including these default values, see
https://docs.kedro.org/en/stable/kedro_project_setup/settings.html."""

# Hooks
from churn_analytics.hooks import SparkHooks  # noqa: E402
HOOKS = (SparkHooks(),)

# Config loader
from kedro.config import OmegaConfigLoader  # noqa: E402
CONFIG_LOADER_CLASS = OmegaConfigLoader
CONFIG_LOADER_ARGS = {
    "base_env": "base",
    "default_run_env": "local",
    "config_patterns": {
        "spark": ["spark*", "spark*/**"],
    }
}

# 🧠 REGISTRA TODOS OS PIPELINES
from churn_analytics.pipeline_registry import register_pipelines
PIPELINE_REGISTRY = register_pipelines()

# Dataset customizado
from churn_analytics.datasets.spark_model_dataset import SparkModelDataset
DATASET_FACTORY = {
    "SparkModelDataset": SparkModelDataset,
}

# Inferencia
from churn_analytics import pipeline_registry
PIPELINE_REGISTRY = pipeline_registry.register_pipelines()

from pyspark.sql import SparkSession

def configure_spark():
    spark = SparkSession.builder.getOrCreate()
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "false")

configure_spark()