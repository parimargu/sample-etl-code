from typing import Dict, Any
from .embedder import T5Embedder

class EmbeddingFactory:
    @staticmethod
    def get_embedder(strategy: str, config: Dict[str, Any]):
        # Default to T5Embedder
        return T5Embedder(config)
