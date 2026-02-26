"""
Embedding service for generating vector embeddings of Telugu text.
Uses bge-m3 model which has excellent multilingual support including Telugu.
"""
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings using bge-m3"""
    
    model = None
    model_name = "BAAI/bge-m3"
    
    def __init__(self):
        self._initialized = False
    
    async def initialize(self):
        """Lazy initialization of the embedding model"""
        if self._initialized:
            return
        
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            self._initialized = True
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    
    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed (can be Telugu, English, or mixed)
            
        Returns:
            Vector embedding as list of floats
        """
        if not self._initialized:
            await self.initialize()
        
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of vector embeddings
        """
        if not self._initialized:
            await self.initialize()
        
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return [emb.tolist() for emb in embeddings]
    
    async def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.
        Uses instruction prefix for better retrieval performance.
        
        Args:
            query: Search query text
            
        Returns:
            Vector embedding optimized for retrieval
        """
        if not self._initialized:
            await self.initialize()
        
        # bge-m3 benefits from instruction prefix for queries
        instruction = "Represent this sentence for searching relevant passages: "
        embedding = self.model.encode(
            instruction + query,
            normalize_embeddings=True,
        )
        return embedding.tolist()


embedding_service = EmbeddingService()
