"""
Reset Qdrant collection - deletes and recreates with correct dimensions.
Use this when changing embedding models or dimensions.

Usage:
    python -m scripts.reset_qdrant
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.vector_db import vector_db


async def reset_collection():
    """Delete and recreate the Qdrant collection"""
    print("Connecting to Qdrant...")
    await vector_db.connect()
    
    try:
        # Try to delete existing collection
        print(f"Deleting collection '{vector_db.collection_name}'...")
        vector_db.client.delete_collection(collection_name=vector_db.collection_name)
        print("Collection deleted successfully")
    except Exception as e:
        print(f"Note: {e}")
    
    # Recreate collection with new dimensions
    print(f"Creating collection with {vector_db.EMBEDDING_DIM} dimensions...")
    from qdrant_client.http.models import Distance, VectorParams
    
    vector_db.client.create_collection(
        collection_name=vector_db.collection_name,
        vectors_config=VectorParams(
            size=vector_db.EMBEDDING_DIM,
            distance=Distance.COSINE,
        ),
    )
    
    print(f"Collection '{vector_db.collection_name}' created successfully!")
    print(f"Dimensions: {vector_db.EMBEDDING_DIM}")
    
    await vector_db.disconnect()


if __name__ == "__main__":
    asyncio.run(reset_collection())
