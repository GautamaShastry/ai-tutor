"""
Data ingestion service for loading Telugu content into the vector database.
"""
import logging
from pathlib import Path
from typing import List, Optional, Type

from app.data.loaders.base import BaseLoader
from app.data.loaders.tatoeba import TatoebaLoader
from app.data.loaders.custom import CustomLoader
from app.data.loaders.samanantar import SamanantatLoader
from app.data.models import ProcessedContent
from app.core.vector_db import vector_db
from app.services.embedding import embedding_service

logger = logging.getLogger(__name__)


class IngestionService:
    """Service for ingesting Telugu learning content into vector storage"""
    
    BATCH_SIZE = 100  # Process embeddings in batches
    
    def __init__(self):
        self.loaders: List[BaseLoader] = []
    
    def add_tatoeba_source(self, data_path: Path) -> bool:
        """Add Tatoeba as a data source"""
        loader = TatoebaLoader(data_path)
        if loader.validate_source():
            self.loaders.append(loader)
            logger.info(f"Added Tatoeba source from {data_path}")
            return True
        logger.warning(f"Invalid Tatoeba source at {data_path}")
        return False
    
    def add_samanantar_source(self, data_path: Path, max_items: int = None) -> bool:
        """
        Add AI4Bharat Samanantar as a data source.
        
        Args:
            data_path: Path to samanantar data
            max_items: Limit number of items (useful for testing)
        """
        loader = SamanantatLoader(data_path, max_items=max_items)
        if loader.validate_source():
            self.loaders.append(loader)
            logger.info(f"Added Samanantar source from {data_path} (max: {max_items or 'all'})")
            return True
        logger.warning(f"Invalid Samanantar source at {data_path}")
        return False
    
    def add_custom_source(
        self,
        data_path: Path,
        source_name: str = "Custom",
        license_info: str = "Custom",
    ) -> bool:
        """Add a custom data source"""
        loader = CustomLoader(data_path, source_name, license_info)
        if loader.validate_source():
            self.loaders.append(loader)
            logger.info(f"Added custom source '{source_name}' from {data_path}")
            return True
        logger.warning(f"Invalid custom source at {data_path}")
        return False
    
    async def ingest_all(self) -> dict:
        """
        Ingest content from all registered sources.
        Returns statistics about the ingestion.
        """
        stats = {
            "total_processed": 0,
            "total_stored": 0,
            "errors": 0,
            "sources": {},
        }
        
        for loader in self.loaders:
            source_stats = await self._ingest_source(loader)
            stats["sources"][loader.source_name] = source_stats
            stats["total_processed"] += source_stats["processed"]
            stats["total_stored"] += source_stats["stored"]
            stats["errors"] += source_stats["errors"]
        
        logger.info(f"Ingestion complete: {stats}")
        return stats
    
    async def _ingest_source(self, loader: BaseLoader) -> dict:
        """Ingest content from a single source"""
        stats = {"processed": 0, "stored": 0, "errors": 0}
        batch: List[ProcessedContent] = []
        
        logger.info(f"Starting ingestion from {loader.source_name}")
        
        async for content in loader.load():
            batch.append(content)
            stats["processed"] += 1
            
            if len(batch) >= self.BATCH_SIZE:
                stored = await self._store_batch(batch)
                stats["stored"] += stored
                stats["errors"] += len(batch) - stored
                batch = []
            
            if stats["processed"] % 1000 == 0:
                logger.info(f"Processed {stats['processed']} items from {loader.source_name}")
        
        # Store remaining items
        if batch:
            stored = await self._store_batch(batch)
            stats["stored"] += stored
            stats["errors"] += len(batch) - stored
        
        logger.info(f"Completed {loader.source_name}: {stats}")
        return stats
    
    async def _store_batch(self, batch: List[ProcessedContent]) -> int:
        """Store a batch of content items with embeddings"""
        stored = 0
        
        try:
            # Generate embeddings for all texts in batch
            texts = [item.text for item in batch]
            embeddings = await embedding_service.embed_texts(texts)
            
            # Store each item with its embedding
            for content, embedding in zip(batch, embeddings):
                try:
                    payload = {
                        "content_type": content.content_type.value,
                        "telugu_text": content.telugu_text,
                        "english_text": content.english_text,
                        "transliteration": content.transliteration,
                        "difficulty": content.difficulty.value,
                        "domains": content.domains,
                        "source": content.source,
                        "license": content.license,
                        "metadata": content.metadata,
                    }
                    
                    await vector_db.upsert_content(
                        content_id=content.id,
                        embedding=embedding,
                        payload=payload,
                    )
                    stored += 1
                except Exception as e:
                    logger.error(f"Failed to store content {content.id}: {e}")
        
        except Exception as e:
            logger.error(f"Failed to generate embeddings for batch: {e}")
        
        return stored


# Singleton instance
ingestion_service = IngestionService()
