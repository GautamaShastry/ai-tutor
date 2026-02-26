"""
Vector database client for RAG-based content retrieval.
Uses Qdrant for storing and searching Telugu learning content embeddings.
"""
from typing import Optional, List
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PointStruct

from app.core.config import settings


class VectorDBClient:
    """Qdrant vector database client for Telugu content retrieval"""
    
    client: Optional[QdrantClient] = None
    collection_name: str = settings.qdrant_collection
    
    # OpenAI text-embedding-3-small dimension
    EMBEDDING_DIM = 1536
    
    async def connect(self):
        """Initialize Qdrant client"""
        self.client = QdrantClient(url=settings.qdrant_url)
        
        # Create collection if it doesn't exist
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.EMBEDDING_DIM,
                    distance=Distance.COSINE,
                ),
            )
    
    async def disconnect(self):
        """Close Qdrant client"""
        if self.client:
            self.client.close()
    
    async def upsert_content(
        self,
        content_id: str,
        embedding: List[float],
        payload: dict,
    ) -> None:
        """
        Insert or update content with its embedding.
        
        Args:
            content_id: Unique identifier for the content
            embedding: Vector embedding of the content
            payload: Metadata including text, domain, category, etc.
        """
        point = PointStruct(
            id=content_id,
            vector=embedding,
            payload=payload,
        )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point],
        )
    
    async def search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        domain_filter: Optional[str] = None,
        category_filter: Optional[str] = None,
    ) -> List[dict]:
        """
        Search for similar content using vector similarity.
        
        Args:
            query_embedding: Query vector
            limit: Maximum number of results
            domain_filter: Optional domain to filter by (office, family, movies)
            category_filter: Optional category to filter by
            
        Returns:
            List of matching content with scores
        """
        # Build filter conditions
        filter_conditions = []
        
        if domain_filter:
            filter_conditions.append(
                models.FieldCondition(
                    key="domain",
                    match=models.MatchValue(value=domain_filter),
                )
            )
        
        if category_filter:
            filter_conditions.append(
                models.FieldCondition(
                    key="category",
                    match=models.MatchValue(value=category_filter),
                )
            )
        
        query_filter = None
        if filter_conditions:
            query_filter = models.Filter(must=filter_conditions)
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
            query_filter=query_filter,
        )
        
        return [
            {
                "id": str(hit.id),
                "score": hit.score,
                "payload": hit.payload,
            }
            for hit in results
        ]
    
    async def delete_content(self, content_id: str) -> None:
        """Delete content by ID"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(points=[content_id]),
        )
    
    async def get_collection_info(self) -> dict:
        """Get collection statistics"""
        info = self.client.get_collection(self.collection_name)
        return {
            "name": self.collection_name,
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
        }


vector_db = VectorDBClient()
