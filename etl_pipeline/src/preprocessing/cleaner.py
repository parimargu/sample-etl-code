from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lower, regexp_replace, trim
from typing import Dict, Any, List
import logging

class TextCleaner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def process(self, df: DataFrame) -> DataFrame:
        """
        Applies cleaning steps to the 'source_text' column.
        Returns DataFrame with 'clean_text' column.
        """
        steps = self.config.get('steps', [])
        
        self.logger.info(f"Applying preprocessing steps: {steps}")
        
        # Start with source_text
        df = df.withColumn("clean_text", col("source_text"))
        
        for step in steps:
            if step == "lowercase":
                df = df.withColumn("clean_text", lower(col("clean_text")))
            elif step == "remove_urls":
                # Regex for URL removal
                url_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
                df = df.withColumn("clean_text", regexp_replace(col("clean_text"), url_pattern, ""))
            elif step == "remove_punctuation":
                # Remove non-alphanumeric characters (keeping spaces)
                df = df.withColumn("clean_text", regexp_replace(col("clean_text"), r"[^a-zA-Z0-9\s]", ""))
            elif step == "trim":
                df = df.withColumn("clean_text", trim(col("clean_text")))
            else:
                self.logger.warning(f"Unknown preprocessing step: {step}")

        return df
