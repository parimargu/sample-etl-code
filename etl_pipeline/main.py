import sys
import os
from pyspark.sql import SparkSession
from etl_pipeline.config.config_loader import ConfigLoader
from etl_pipeline.src.utils.logger import setup_logger
from etl_pipeline.src.pipeline import Pipeline

def main():
    # Setup Logger
    logger = setup_logger("NLP_ETL_Pipeline")
    
    # Load Config
    config_path = os.environ.get("PIPELINE_CONFIG", "etl_pipeline/config/pipeline.yaml")
    logger.info(f"Loading configuration from {config_path}")
    
    try:
        config_loader = ConfigLoader(config_path)
        config = config_loader.get_config()
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        sys.exit(1)

    # Initialize Spark
    logger.info("Initializing Spark Session")
    spark = SparkSession.builder \
        .appName(config.get('pipeline', {}).get('name', 'NLP_ETL')) \
        .getOrCreate()
    
    # Run Pipeline
    try:
        pipeline = Pipeline(spark, config)
        pipeline.run()
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)
        sys.exit(1)
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
