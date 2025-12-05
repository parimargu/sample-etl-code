from pyspark.sql import SparkSession, DataFrame
from typing import Dict, Any
import logging
import os

class FileSource:
    def __init__(self, spark: SparkSession, config: Dict[str, Any]):
        self.spark = spark
        self.config = config
        self.logger = logging.getLogger(__name__)

    def read(self) -> DataFrame:
        """
        Reads data from files (CSV/JSON).
        Expected config keys: 'path', 'format'.
        """
        path = self.config.get('path')
        fmt = self.config.get('format', 'csv')

        if not path:
            raise ValueError("File configuration must provide 'path'.")

        try:
            self.logger.info(f"Reading {fmt} files from: {path}")
            
            reader = self.spark.read.format(fmt)
            
            if fmt == 'csv':
                reader = reader.option("header", "true").option("inferSchema", "true")
            
            df = reader.load(path)
            
            count = df.count()
            self.logger.info(f"Successfully read {count} rows from {path}")

            # Validate required columns
            required_columns = ['doc_id', 'source_text']
            for col in required_columns:
                if col not in df.columns:
                    self.logger.error(f"Missing required column: {col}")
                    raise ValueError(f"File source missing required column: {col}")

            return df.select(*required_columns)

        except Exception as e:
            self.logger.error(f"Error reading files: {e}")
            raise
