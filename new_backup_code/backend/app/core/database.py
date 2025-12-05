import sqlite3
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        conn = sqlite3.connect(settings.SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        # Load sqlite-vec extension if needed
        # conn.enable_load_extension(True)
        # conn.load_extension("vec0")
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise
