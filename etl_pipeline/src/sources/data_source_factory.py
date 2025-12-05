from pyspark.sql import SparkSession
from typing import Dict, Any
from .hive_source import HiveSource
from .file_source import FileSource

class DataSourceFactory:
    @staticmethod
    def get_source(source_type: str, spark: SparkSession, config: Dict[str, Any]):
        if source_type == 'hive':
            return HiveSource(spark, config)
        elif source_type == 'file':
            return FileSource(spark, config)
        else:
            raise ValueError(f"Unknown source type: {source_type}")
