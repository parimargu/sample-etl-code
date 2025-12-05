import pytest
from pyspark.sql import SparkSession
from etl_pipeline.src.preprocessing.cleaner import TextCleaner

@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("TestPreprocessing") \
        .getOrCreate()
    yield spark
    spark.stop()

def test_text_cleaner(spark):
    data = [("1", "Hello World! https://example.com")]
    df = spark.createDataFrame(data, ["doc_id", "source_text"])
    
    config = {
        "steps": ["lowercase", "remove_urls", "remove_punctuation", "trim"]
    }
    
    cleaner = TextCleaner(config)
    processed_df = cleaner.process(df)
    
    assert "clean_text" in processed_df.columns
    
    row = processed_df.collect()[0]
    # "hello world! " -> "hello world " -> "hello world " -> "hello world"
    # Note: remove_punctuation removes '!'
    assert row["clean_text"] == "hello world"

def test_text_cleaner_no_steps(spark):
    data = [("1", "Hello World")]
    df = spark.createDataFrame(data, ["doc_id", "source_text"])
    
    cleaner = TextCleaner({})
    processed_df = cleaner.process(df)
    
    row = processed_df.collect()[0]
    assert row["clean_text"] == "Hello World"
