from pyspark.sql import DataFrame
from typing import Dict, Any
import logging
import sqlite3
import json
import struct

class SQLiteSink:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_path = config.get('db_path', 'data/processed/vector_db.sqlite')
        self.logger = logging.getLogger(__name__)
        self._initialize_db()

    def _initialize_db(self):
        """Creates tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enable sqlite-vec if available (assuming it's loaded or compiled in)
        # For now, we'll just create standard tables and a vector table
        # Note: In a real env, we'd load the extension: conn.enable_load_extension(True); conn.load_extension("vec0")
        
        # Source Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS source_tbl (
                doc_id TEXT PRIMARY KEY,
                source_text TEXT
            )
        ''')
        
        # Preprocessing Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preprocessing_tbl (
                doc_id TEXT PRIMARY KEY,
                clean_text TEXT,
                FOREIGN KEY(doc_id) REFERENCES source_tbl(doc_id)
            )
        ''')
        
        # Chunking Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunking_tbl (
                chunk_id TEXT PRIMARY KEY,
                doc_id TEXT,
                chunk_text TEXT,
                sequence_no INTEGER,
                FOREIGN KEY(doc_id) REFERENCES source_tbl(doc_id)
            )
        ''')
        
        # Embedding Table (using sqlite-vec virtual table if possible, else standard blob/text)
        # For this implementation, we will use a standard table to store vectors as JSON or BLOB
        # and assume the vector search happens via application logic or loaded extension later.
        # If sqlite-vec is strictly required for *storage*, we'd use:
        # CREATE VIRTUAL TABLE vec_items USING vec0(embedding float[768]);
        
        # We'll create a standard table for metadata + vector
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS embedding_tbl (
                chunk_id TEXT PRIMARY KEY,
                embedding BLOB,
                FOREIGN KEY(chunk_id) REFERENCES chunking_tbl(chunk_id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def write(self, df: DataFrame, stage_name: str):
        """
        Writes data to the appropriate SQLite table based on stage.
        """
        self.logger.info(f"Writing {stage_name} output to SQLite")
        
        rows = df.collect()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            if stage_name == 'source':
                data = [(r['doc_id'], r['source_text']) for r in rows]
                cursor.executemany('INSERT OR REPLACE INTO source_tbl VALUES (?, ?)', data)
            
            elif stage_name == 'preprocessing':
                data = [(r['doc_id'], r['clean_text']) for r in rows]
                cursor.executemany('INSERT OR REPLACE INTO preprocessing_tbl VALUES (?, ?)', data)
                
            elif stage_name == 'chunking':
                data = [(r['chunk_id'], r['doc_id'], r['chunk_text'], r['sequence_no']) for r in rows]
                cursor.executemany('INSERT OR REPLACE INTO chunking_tbl VALUES (?, ?, ?, ?)', data)
                
            elif stage_name == 'embedding':
                # Serialize embedding list to bytes or JSON
                # sqlite-vec usually expects raw bytes for float32 array
                data = []
                for r in rows:
                    emb_list = r['embedding']
                    # Pack floats into bytes
                    emb_bytes = struct.pack(f'{len(emb_list)}f', *emb_list)
                    data.append((r['chunk_id'], emb_bytes))
                
                cursor.executemany('INSERT OR REPLACE INTO embedding_tbl VALUES (?, ?)', data)
                
            conn.commit()
        except Exception as e:
            self.logger.error(f"Error writing to SQLite: {e}")
            raise
        finally:
            conn.close()
