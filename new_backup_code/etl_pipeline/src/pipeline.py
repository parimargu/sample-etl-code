from pyspark.sql import SparkSession
from typing import Dict, Any
import logging
from .sources.data_source_factory import DataSourceFactory
from .preprocessing.preprocessing_factory import PreprocessingFactory
from .chunking.chunking_factory import ChunkingFactory
from .embedding.embedding_factory import EmbeddingFactory
from .targets.target_factory import TargetFactory

class Pipeline:
    def __init__(self, spark: SparkSession, config: Dict[str, Any]):
        self.spark = spark
        self.config = config
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.logger.info("Starting Pipeline Execution")

        # 1. Data Source
        source_config = self.config.get('sources', {})
        source_type = self.config.get('source_type', 'file')
        
        self.logger.info(f"Using source type: {source_type}")
        
        if source_type == 'hive':
            s_conf = source_config.get('hive', {})
        elif source_type == 'file':
            s_conf = source_config.get('file', {})
        else:
            raise ValueError(f"Unsupported source_type: {source_type}")

        self.logger.info(f"Using source: {source_type}")
        source = DataSourceFactory.get_source(source_type, self.spark, s_conf)
        df = source.read()
        
        # Save Source Output
        self._save_output(df, 'source')

        # 2. Preprocessing
        prep_config = self.config.get('preprocessing', {})
        preprocessor = PreprocessingFactory.get_preprocessor('standard', prep_config)
        df_clean = preprocessor.process(df)
        
        # Save Preprocessing Output
        self._save_output(df_clean, 'preprocessing')

        # 3. Chunking
        chunk_config = self.config.get('chunking', {})
        chunker = ChunkingFactory.get_chunker('fixed_size', chunk_config)
        df_chunked = chunker.process(df_clean)
        
        # Save Chunking Output
        self._save_output(df_chunked, 'chunking')

        # 4. Embedding
        emb_config = self.config.get('embedding', {})
        embedder = EmbeddingFactory.get_embedder('t5', emb_config)
        df_embedded = embedder.process(df_chunked)
        
        # Save Embedding Output
        self._save_output(df_embedded, 'embedding')

        self.logger.info("Pipeline Execution Completed")

    def _save_output(self, df, stage_name):
        target_config = self.config.get('targets', {})
        
        # Save to Local Storage
        if 'local_storage' in target_config:
            ls_sink = TargetFactory.get_target('local_storage', target_config['local_storage'])
            ls_sink.write(df, stage_name)
            
        # Save to SQLite (only for specific stages usually, but we'll try all that match schema)
        if 'sqlite' in target_config:
            sqlite_sink = TargetFactory.get_target('sqlite', target_config['sqlite'])
            try:
                sqlite_sink.write(df, stage_name)
            except Exception as e:
                self.logger.warning(f"Could not write stage {stage_name} to SQLite: {e}")
