from typing import List, Dict, Any
from app.core.database import get_db_connection
from app.core.config import settings
from sentence_transformers import SentenceTransformer
import struct
import numpy as np
import logging

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self):
        # Load model once
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Performs vector search for the query.
        """
        # 1. Generate embedding for query
        query_embedding = self.model.encode(query).tolist()
        
        # 2. Search in SQLite
        # If using sqlite-vec:
        # sql = "SELECT chunk_id, distance FROM embedding_tbl WHERE embedding MATCH ? ORDER BY distance LIMIT ?"
        # params = (serialize(query_embedding), limit)
        
        # Since we don't have the extension guaranteed, we'll do a brute-force cosine similarity in Python
        # This is slow for large data but works for this demo.
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT chunk_id, embedding FROM embedding_tbl")
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                chunk_id = row['chunk_id']
                emb_blob = row['embedding']
                
                # Unpack embedding
                # Assuming 768 dimensions for T5-base, but let's be dynamic
                # float is 4 bytes
                dim = len(emb_blob) // 4
                emb_vec = struct.unpack(f'{dim}f', emb_blob)
                
                # Calculate Cosine Similarity
                score = self._cosine_similarity(query_embedding, emb_vec)
                results.append((chunk_id, score))
            
            # Sort by score desc
            results.sort(key=lambda x: x[1], reverse=True)
            top_results = results[:limit]
            
            # Fetch details for top results
            final_response = []
            for chunk_id, score in top_results:
                # Get chunk text and doc_id
                cursor.execute("SELECT doc_id, chunk_text FROM chunking_tbl WHERE chunk_id = ?", (chunk_id,))
                chunk_data = cursor.fetchone()
                
                if chunk_data:
                    # Get doc metadata (department) - assuming it's in source text or we parse it
                    # For now just return what we have
                    final_response.append({
                        "chunk_id": chunk_id,
                        "doc_id": chunk_data['doc_id'],
                        "text": chunk_data['chunk_text'],
                        "score": float(score)
                    })
            
            return final_response
            
        finally:
            conn.close()

    def get_document(self, doc_id: str) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT source_text FROM source_tbl WHERE doc_id = ?", (doc_id,))
            row = cursor.fetchone()
            if row:
                return {"doc_id": doc_id, "text": row['source_text']}
            return None
        finally:
            conn.close()

    def _cosine_similarity(self, v1, v2):
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        return dot_product / (norm_v1 * norm_v2)
