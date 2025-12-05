import pytest
from pyspark.sql import SparkSession
from etl_pipeline.src.targets.local_storage import LocalStorageSink
from etl_pipeline.src.targets.sqlite_sink import SQLiteSink
import os
import sqlite3
import struct

@pytest.fixture(scope="session")
def spark():
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("TestTargets") \
        .getOrCreate()
    yield spark
    spark.stop()

def test_local_storage_sink(spark, tmp_path):
    data = [("1", "text")]
    df = spark.createDataFrame(data, ["doc_id", "source_text"])
    
    config = {"path": str(tmp_path)}
    sink = LocalStorageSink(config)
    sink.write(df, "source")
    
    # Check if file exists
    # path/date/source/output_*.pickle
    import glob
    files = glob.glob(f"{tmp_path}/*/*/*.pickle")
    assert len(files) > 0

def test_sqlite_sink(spark, tmp_path):
    db_path = tmp_path / "test.db"
    config = {"db_path": str(db_path)}
    
    sink = SQLiteSink(config)
    
    # Test Source Write
    data = [("1", "text")]
    df = spark.createDataFrame(data, ["doc_id", "source_text"])
    sink.write(df, "source")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM source_tbl")
    rows = cursor.fetchall()
    assert len(rows) == 1
    assert rows[0] == ("1", "text")
    
    # Test Embedding Write
    data_emb = [("1:0", [0.1, 0.2])]
    df_emb = spark.createDataFrame(data_emb, ["chunk_id", "embedding"])
    sink.write(df_emb, "embedding")
    
    cursor.execute("SELECT * FROM embedding_tbl")
    rows = cursor.fetchall()
    assert len(rows) == 1
    assert rows[0][0] == "1:0"
    
    # Verify blob
    emb_bytes = rows[0][1]
    emb_list = struct.unpack('2f', emb_bytes)
    assert pytest.approx(emb_list[0]) == 0.1
    
    conn.close()
