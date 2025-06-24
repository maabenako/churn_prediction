from kedro.io import AbstractDataset
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession


class SparkModelDataset(AbstractDataset):
    def __init__(self, filepath: str, save_args=None, load_args=None):
        self._filepath = filepath
        self._save_args = save_args or {}
        self._load_args = load_args or {}
        self._spark = SparkSession.builder.getOrCreate()

    def _load(self) -> PipelineModel:
        return PipelineModel.load(self._filepath)

    def _save(self, model: PipelineModel) -> None:
        model.write().overwrite().save(self._filepath)

    def _describe(self) -> dict:
        return dict(filepath=self._filepath)
