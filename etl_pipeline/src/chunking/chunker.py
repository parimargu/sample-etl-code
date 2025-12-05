from pyspark.sql import DataFrame
from pyspark.sql.functions import udf, explode, col
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, IntegerType
from typing import Dict, Any, List
import logging
import math

class FixedSizeChunker:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.target_chunk_size = config.get('chunk_size', 512)
        self.overlap = config.get('overlap', 0)
        self.logger = logging.getLogger(__name__)

    def process(self, df: DataFrame) -> DataFrame:
        """
        Chunks the 'clean_text' column.
        Returns DataFrame with 'chunk_text' and 'chunk_id'.
        """
        self.logger.info(f"Chunking text with target size {self.target_chunk_size} and overlap {self.overlap}")

        # Define schema for the UDF return type
        chunk_schema = ArrayType(StructType([
            StructField("chunk_id", StringType(), False),
            StructField("chunk_text", StringType(), False),
            StructField("sequence_no", IntegerType(), False)
        ]))

        # UDF for chunking logic
        @udf(returnType=chunk_schema)
        def chunk_text_udf(doc_id: str, text: str):
            if not text:
                return []
            
            words = text.split()
            total_tokens = len(words)
            
            if total_tokens <= self.target_chunk_size:
                return [{"chunk_id": f"{doc_id}:0", "chunk_text": text, "sequence_no": 0}]
            
            # Smoothing Logic: Calculate optimal chunk size
            # We want roughly equal sized chunks
            num_chunks = math.ceil(total_tokens / self.target_chunk_size)
            optimal_chunk_size = math.ceil(total_tokens / num_chunks)
            
            chunks = []
            for i in range(num_chunks):
                start_idx = i * optimal_chunk_size
                # Add overlap if needed, but for strict smoothing we might want to be careful
                # Here we prioritize the smoothing requirement over overlap for simplicity unless specified
                # If overlap is needed, we would adjust start/end indices
                
                end_idx = min((i + 1) * optimal_chunk_size, total_tokens)
                
                # If overlap is strictly required:
                if self.overlap > 0 and i > 0:
                    start_idx = max(0, start_idx - self.overlap)
                
                chunk_words = words[start_idx:end_idx]
                chunk_str = " ".join(chunk_words)
                
                chunks.append({
                    "chunk_id": f"{doc_id}:{i}",
                    "chunk_text": chunk_str,
                    "sequence_no": i
                })
            
            return chunks

        # Apply UDF and explode
        df_chunked = df.withColumn("chunks", chunk_text_udf(col("doc_id"), col("clean_text")))
        df_exploded = df_chunked.select(
            col("doc_id"), 
            explode(col("chunks")).alias("chunk_data")
        )
        
        # Flatten structure
        final_df = df_exploded.select(
            col("doc_id"),
            col("chunk_data.chunk_id").alias("chunk_id"),
            col("chunk_data.chunk_text").alias("chunk_text"),
            col("chunk_data.sequence_no").alias("sequence_no")
        )

        return final_df
