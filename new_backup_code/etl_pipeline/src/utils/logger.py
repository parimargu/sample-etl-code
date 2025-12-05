import logging
import os
from datetime import datetime

def setup_logger(name: str, log_dir: str = "logs", level: int = logging.INFO) -> logging.Logger:
    """
    Sets up a logger with console and file handlers.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"pipeline_{timestamp}.log")

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Configure root logger or package logger
    # If name is provided, use it, but also ensure basic config is set for the app
    
    # We will configure the 'etl_pipeline' logger which is the parent of all modules
    # assuming modules use logging.getLogger(__name__) where __name__ starts with etl_pipeline
    
    # If name is passed as "NLP_ETL_Pipeline", it might be for the main script only.
    # To fix the issue, we will configure the root logger if name is None, or the specific logger.
    # But better yet, let's configure the 'etl_pipeline' logger.
    
    logger = logging.getLogger("etl_pipeline")
    logger.setLevel(level)
    
    # Also configure the logger requested (e.g. for main script)
    if name != "etl_pipeline":
        specific_logger = logging.getLogger(name)
        specific_logger.setLevel(level)
        # We can attach handlers to root or just to this one. 
        # But to ensure all modules log, we attach to 'etl_pipeline'
    
    # Avoid adding handlers multiple times
    if not logger.handlers:
        # File Handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    # If the requested name is different, return that logger, 
    # but make sure it propagates or has handlers if it's not a child.
    # If main uses "NLP_ETL_Pipeline", it is NOT a child of "etl_pipeline".
    # So we should return the 'etl_pipeline' logger or configure both.
    
    # Simplest fix: Return the 'etl_pipeline' logger and use that in main, 
    # OR configure the root logger.
    
    # Let's configure the ROOT logger to catch everything
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
    return logging.getLogger(name)
