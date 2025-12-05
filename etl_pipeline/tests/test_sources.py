import pytest
from pyspark.sql import SparkSession
from etl_pipeline.src.sources.file_source import FileSource
from etl_pipeline.src.sources.data_source_factory import DataSourceFactory
import os
import shutil

@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("TestSources") \
        .getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture
def sample_data_dir(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Create sample CSV
    csv_file = data_dir / "test.csv"
    with open(csv_file, "w") as f:
        f.write("doc_id,source_text,other_col\n")
        f.write("1,This is a test document.,ignore\n")
        f.write("2,Another document.,ignore\n")
        
    return str(data_dir)

def test_file_source_read(spark, sample_data_dir):
    config = {"path": sample_data_dir, "format": "csv"}
    source = FileSource(spark, config)
    df = source.read()
    
    assert df.count() == 2
    assert "doc_id" in df.columns
    assert "source_text" in df.columns
    
    rows = df.collect()
    assert rows[0]["doc_id"] == 1
    assert rows[0]["source_text"] == "This is a test document."

def test_factory_get_source(spark):
    source = DataSourceFactory.get_source("file", spark, {"path": "dummy"})
    assert isinstance(source, FileSource)

def test_file_source_missing_columns(spark, tmp_path):
    # Create invalid CSV
    csv_file = tmp_path / "invalid.csv"
    with open(csv_file, "w") as f:
        f.write("id,text\n") # Wrong column names
        f.write("1,test\n")
        
    config = {"path": str(csv_file), "format": "csv"}
    source = FileSource(spark, config)
    
    with pytest.raises(ValueError, match="missing required column"):
        source.read()
