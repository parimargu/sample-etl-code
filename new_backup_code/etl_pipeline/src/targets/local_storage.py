from pyspark.sql import DataFrame
from typing import Dict, Any
import logging
import os
from datetime import datetime
import pickle

class LocalStorageSink:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_path = config.get('path', 'data/processed')
        self.logger = logging.getLogger(__name__)

    def write(self, df: DataFrame, stage_name: str):
        """
        Writes DataFrame to local storage as pickle files.
        Organized by date and stage.
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_dir = os.path.join(self.base_path, date_str, stage_name)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"output_{timestamp}.pickle"
        output_path = os.path.join(output_dir, filename)
        
        self.logger.info(f"Saving {stage_name} output to {output_path}")
        
        # Collect data to driver to pickle (Warning: only for reasonable data sizes)
        # For large data, we should use parquet/avro, but requirement says pickle
        data = df.collect()
        
        try:
            with open(output_path, 'wb') as f:
                pickle.dump(data, f)
            self.logger.info(f"Successfully saved {len(data)} records to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving pickle file: {e}")
            raise
