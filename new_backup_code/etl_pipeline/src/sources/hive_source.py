from pyspark.sql import SparkSession, DataFrame
from typing import Dict, Any
import logging

class HiveSource:
    def __init__(self, spark: SparkSession, config: Dict[str, Any]):
        self.spark = spark
        self.config = config
        self.logger = logging.getLogger(__name__)

    def read(self) -> DataFrame:
        """
        Reads data from Hive based on configuration.
        Expected config keys: 'table_name' or 'query'.
        """
        table_name = self.config.get('table_name')
        query = self.config.get('query')

        try:
            if query:
                self.logger.info(f"Reading from Hive using query: {query}")
                df = self.spark.sql(query)
            elif table_name:
                self.logger.info(f"Reading from Hive table: {table_name}")
                df = self.spark.table(table_name)
            else:
                raise ValueError("Hive configuration must provide 'table_name' or 'query'.")

            count = df.count()
            self.logger.info(f"Successfully read {count} rows from Hive")

            # Validate required columns
            required_columns = ['doc_id', 'source_text']
            for col in required_columns:
                if col not in df.columns:
                    self.logger.error(f"Missing required column: {col}")
                    raise ValueError(f"Hive source missing required column: {col}")

            return df.select(*required_columns)

        except Exception as e:
            self.logger.error(f"Error reading from Hive: {e}")
            raise
