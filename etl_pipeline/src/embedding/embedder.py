from pyspark.sql import DataFrame
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import ArrayType, FloatType
from typing import Dict, Any, Iterator
import logging
import pandas as pd

class T5Embedder:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get('model_name', 'sentence-transformers/sentence-t5-base')
        self.logger = logging.getLogger(__name__)

    def process(self, df: DataFrame) -> DataFrame:
        """
        Generates embeddings for 'chunk_text'.
        Returns DataFrame with 'embedding' column.
        """
        self.logger.info(f"Generating embeddings using model: {self.model_name}")
        
        # We need to capture the model name in the closure
        model_name = self.model_name

        @pandas_udf(ArrayType(FloatType()))
        def predict_embedding(texts: pd.Series) -> pd.Series:
            # Import inside UDF to avoid serialization issues
            from sentence_transformers import SentenceTransformer
            import torch
            
            # Load model (this happens once per batch execution in Pandas UDF)
            # Ideally we cache this, but for simplicity in this setup:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = SentenceTransformer(model_name, device=device)
            
            embeddings = model.encode(texts.tolist(), show_progress_bar=False)
            return pd.Series(embeddings.tolist())

        return df.withColumn("embedding", predict_embedding("chunk_text"))
