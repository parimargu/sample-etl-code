import pytest
from pyspark.sql import SparkSession
from etl_pipeline.src.pipeline import Pipeline
from unittest.mock import MagicMock, patch
import os
import shutil

@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("TestPipeline") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture
def test_config(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Create sample CSV
    csv_file = data_dir / "test.csv"
    with open(csv_file, "w") as f:
        f.write("doc_id,source_text\n")
        f.write("1,Test document.\n")
        
    output_dir = tmp_path / "output"
    db_path = tmp_path / "test.db"
    
    return {
        "sources": {
            "file": {"path": str(csv_file), "format": "csv"}
        },
        "preprocessing": {"steps": ["lowercase"]},
        "chunking": {"chunk_size": 10},
        "embedding": {"model_name": "test"},
        "targets": {
            "local_storage": {"path": str(output_dir)},
            "sqlite": {"db_path": str(db_path)}
        }
    }

def test_pipeline_run(spark, test_config):
    # Mock embedding model setup is not needed here as we mock the factory
    # mock_model = MagicMock()
    # mock_st.return_value = mock_model
    # mock_model.encode.return_value = [[0.1, 0.2]]
    
    # We need to patch where it is imported in the UDF, which is hard.
    # So we might need to rely on the fact that we can't easily run the full UDF with mocks in local mode 
    # without the real library or careful patching.
    # For this test, we will assume the real library is not present or we want to skip the actual UDF execution 
    # if we can't mock it easily.
    # BUT, since we are in a controlled environment, let's try to run it. 
    # If sentence-transformers is not installed, this will fail.
    # We'll assume it is installed or we catch the error.
    
    try:
        pipeline = Pipeline(spark, test_config)
        # We need to patch the Embedder process method to avoid UDF complexity if we want a fast test
        # But let's try to patch the Factory to return a mock embedder
        
        with patch('etl_pipeline.src.embedding.embedding_factory.EmbeddingFactory.get_embedder') as mock_factory:
            mock_embedder = MagicMock()
            # Mock process to return a DF with embeddings
            def mock_process(df):
                from pyspark.sql.functions import lit
                return df.withColumn("embedding", lit([0.1, 0.2]))
            
            mock_embedder.process.side_effect = mock_process
            mock_factory.return_value = mock_embedder
            
            pipeline.run()
            
            # Check if outputs exist
            # Local storage
            out_path = test_config['targets']['local_storage']['path']
            assert os.path.exists(out_path)
            
            # SQLite
            db_path = test_config['targets']['sqlite']['db_path']
            assert os.path.exists(db_path)
            
    except ImportError:
        pytest.skip("Dependencies missing")
