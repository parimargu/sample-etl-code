from typing import Dict, Any
from .cleaner import TextCleaner

class PreprocessingFactory:
    @staticmethod
    def get_preprocessor(strategy: str, config: Dict[str, Any]):
        # Currently only supports 'standard' strategy which maps to TextCleaner
        # But designed to be extensible
        if strategy == 'standard':
            return TextCleaner(config)
        else:
            # Default to TextCleaner if strategy not found or just use it as base
            return TextCleaner(config)
