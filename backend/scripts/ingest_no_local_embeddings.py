"""
Ingestion script that uses OpenAI embeddings API instead of local models.
This avoids PyTorch DLL issues on Windows.

Usage:
    Set OPENAI_API_KEY environment variable
    python -m scripts.ingest_no_local_embeddings --source custom --path ./data/sample
"""
import asyncio
import argparse
from pathlib import Path
import sys
import os

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.data.loaders.custom import CustomLoader
from app.data.loaders.tatoeba import TatoebaLoader
from app.data.loaders.samanantar import SamanantatLoader
from app.core.vector_db import vector_db


class SimpleEmbeddingService:
    """Simple embedding service using OpenAI API"""
    
    def __init__(self):
        # Try to get API key from environment or config
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # If not in env, try loading from .env file
        if not self.api_key:
            from dotenv import load_dotenv
            load_dotenv()
            self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not set. Using dummy embeddings for testing.")
            self.use_dummy = True
        else:
            print(f"Using OpenAI embeddings (key: ...{self.api_key[-4:]})")
            self.use_dummy = False
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
    
    async def embed_texts(self, texts):
        """Generate embeddings for texts"""
        if self.use_dummy:
            # Return dummy embeddings (1536 dimensions, all zeros)
            return [[0.0] * 1536 for _ in texts]
        
        # Truncate very long texts to avoid token limit
        max_chars = 8000  # Conservative limit
        truncated_texts = [text[:max_chars] if len(text) > max_chars else text for text in texts]
        
        # Use OpenAI embeddings
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=truncated_texts
        )
        return [item.embedding for item in response.data]


async def ingest_data(source_type, data_path, max_items=None):
    """Ingest data with simple embeddings"""
    
    print("Initializing services...")
    await vector_db.connect()
    
    embedding_service = SimpleEmbeddingService()
    
    # Create loader
    if source_type == "custom":
        loader = CustomLoader(data_path)
    elif source_type == "tatoeba":
        loader = TatoebaLoader(data_path)
    elif source_type == "samanantar":
        loader = SamanantatLoader(data_path, max_items=max_items)
    else:
        print(f"Unknown source type: {source_type}")
        return
    
    if not loader.validate_source():
        print(f"Invalid data source at {data_path}")
        return
    
    print(f"Loading content from {loader.source_name}...")
    
    batch = []
    batch_size = 50  # Reduced to avoid token limits
    total_processed = 0
    total_stored = 0
    
    async for content in loader.load():
        batch.append(content)
        total_processed += 1
        
        if len(batch) >= batch_size:
            # Process batch
            texts = [item.text for item in batch]
            embeddings = await embedding_service.embed_texts(texts)
            
            # Store
            for content_item, embedding in zip(batch, embeddings):
                try:
                    payload = {
                        "content_type": content_item.content_type.value,
                        "telugu_text": content_item.telugu_text,
                        "english_text": content_item.english_text,
                        "transliteration": content_item.transliteration,
                        "difficulty": content_item.difficulty.value,
                        "domains": content_item.domains,
                        "source": content_item.source,
                        "license": content_item.license,
                        "metadata": content_item.metadata,
                    }
                    
                    await vector_db.upsert_content(
                        content_id=content_item.id,
                        embedding=embedding,
                        payload=payload,
                    )
                    total_stored += 1
                except Exception as e:
                    print(f"Error storing item: {e}")
            
            batch = []
            print(f"  Processed {total_processed} items, stored {total_stored}")
    
    # Process remaining
    if batch:
        texts = [item.text for item in batch]
        embeddings = await embedding_service.embed_texts(texts)
        
        for content_item, embedding in zip(batch, embeddings):
            try:
                payload = {
                    "content_type": content_item.content_type.value,
                    "telugu_text": content_item.telugu_text,
                    "english_text": content_item.english_text,
                    "transliteration": content_item.transliteration,
                    "difficulty": content_item.difficulty.value,
                    "domains": content_item.domains,
                    "source": content_item.source,
                    "license": content_item.license,
                    "metadata": content_item.metadata,
                }
                
                await vector_db.upsert_content(
                    content_id=content_item.id,
                    embedding=embedding,
                    payload=payload,
                )
                total_stored += 1
            except Exception as e:
                print(f"Error storing item: {e}")
    
    print(f"\n=== Ingestion Complete ===")
    print(f"Total processed: {total_processed}")
    print(f"Total stored: {total_stored}")
    
    info = await vector_db.get_collection_info()
    print(f"Vector DB collection '{info['name']}': {info['points_count']} items")
    
    await vector_db.disconnect()


async def main():
    parser = argparse.ArgumentParser(description="Ingest Telugu content (no local embeddings)")
    parser.add_argument("--source", type=str, required=True, choices=["tatoeba", "samanantar", "custom"])
    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--max-items", type=int, default=None)
    
    args = parser.parse_args()
    data_path = Path(args.path)
    
    if not data_path.exists():
        print(f"Error: Data path does not exist: {data_path}")
        sys.exit(1)
    
    try:
        await ingest_data(args.source, data_path, args.max_items)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
