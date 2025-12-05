from typing import Dict, Any
from .chunker import FixedSizeChunker

class ChunkingFactory:
    @staticmethod
    def get_chunker(strategy: str, config: Dict[str, Any]):
        if strategy == 'fixed_size':
            return FixedSizeChunker(config)
        else:
            return FixedSizeChunker(config)
