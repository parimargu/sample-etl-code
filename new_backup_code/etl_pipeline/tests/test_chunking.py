import pytest
from pyspark.sql import SparkSession
from etl_pipeline.src.chunking.chunker import FixedSizeChunker

@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("TestChunking") \
        .getOrCreate()
    yield spark
    spark.stop()

def test_chunking_smoothing(spark):
    # Create a text with 10 words
    text = "word " * 10
    data = [("1", text.strip())]
    df = spark.createDataFrame(data, ["doc_id", "clean_text"])
    
    # Target size 4 -> should result in 3 chunks (10/4 = 2.5 -> 3)
    # Optimal size -> 10/3 = 3.33 -> 4 words per chunk roughly
    # Chunk 1: 4 words, Chunk 2: 4 words, Chunk 3: 2 words (or similar distribution)
    config = {"chunk_size": 4, "overlap": 0}
    chunker = FixedSizeChunker(config)
    chunked_df = chunker.process(df)
    
    rows = chunked_df.collect()
    assert len(rows) == 3
    
    # Check smoothing - lengths should be close
    lengths = [len(r["chunk_text"].split()) for r in rows]
    assert max(lengths) - min(lengths) <= 1 # Difference should be small

def test_chunking_small_text(spark):
    text = "small text"
    data = [("1", text)]
    df = spark.createDataFrame(data, ["doc_id", "clean_text"])
    
    config = {"chunk_size": 512}
    chunker = FixedSizeChunker(config)
    chunked_df = chunker.process(df)
    
    rows = chunked_df.collect()
    assert len(rows) == 1
    assert rows[0]["chunk_id"] == "1:0"
