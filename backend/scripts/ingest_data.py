"""
CLI script for ingesting Telugu learning content.

Usage:
    python -m scripts.ingest_data --source tatoeba --path ./data/tatoeba
    python -m scripts.ingest_data --source samanantar --path ./data/samanantar --max-items 10000
    python -m scripts.ingest_data --source custom --path ./data/custom --name "My Content"
    python -m scripts.ingest_data --source custom --path ./data/sample --dry-run
"""
import asyncio
import argparse
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


async def main():
    parser = argparse.ArgumentParser(description="Ingest Telugu learning content")
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        choices=["tatoeba", "samanantar", "custom", "all"],
        help="Data source type",
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Path to data directory",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="Custom",
        help="Source name (for custom sources)",
    )
    parser.add_argument(
        "--license",
        type=str,
        default="Custom",
        help="License info (for custom sources)",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=None,
        help="Maximum items to ingest (useful for large datasets like Samanantar)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview content without storing (no Qdrant needed)",
    )
    
    args = parser.parse_args()
    data_path = Path(args.path)
    
    if not data_path.exists():
        print(f"Error: Data path does not exist: {data_path}")
        sys.exit(1)
    
    if args.dry_run:
        await dry_run(args, data_path)
    else:
        await full_ingest(args, data_path)


async def dry_run(args, data_path: Path):
    """Preview content without storing to vector DB"""
    from app.data.loaders.custom import CustomLoader
    from app.data.loaders.tatoeba import TatoebaLoader
    from app.data.loaders.samanantar import SamanantatLoader
    
    print(f"=== DRY RUN: Previewing content from {data_path} ===\n")
    
    if args.source == "custom":
        loader = CustomLoader(data_path, args.name, args.license)
    elif args.source == "tatoeba":
        loader = TatoebaLoader(data_path)
    elif args.source == "samanantar":
        loader = SamanantatLoader(data_path, max_items=args.max_items or 100)
    else:
        print("Dry run only supports 'custom', 'tatoeba', and 'samanantar' sources")
        return
    
    if not loader.validate_source():
        print(f"Error: Invalid data source at {data_path}")
        return
    
    count = 0
    async for content in loader.load():
        count += 1
        if count <= 10:  # Show first 10 items
            print(f"[{content.content_type.value}] {content.difficulty.value}")
            print(f"  Telugu: {content.telugu_text}")
            print(f"  English: {content.english_text}")
            if content.transliteration:
                print(f"  Translit: {content.transliteration}")
            print()
    
    print(f"=== Total items found: {count} ===")
    print("\nTo actually ingest, run without --dry-run flag")
    print("Make sure Qdrant is running: docker-compose up -d qdrant")


async def full_ingest(args, data_path: Path):
    """Full ingestion with vector DB storage"""
    from app.data.ingestion import ingestion_service
    from app.core.vector_db import vector_db
    from app.services.embedding import embedding_service
    
    print("Initializing services...")
    
    try:
        await vector_db.connect()
    except Exception as e:
        print(f"Error: Could not connect to Qdrant: {e}")
        print("\nMake sure Qdrant is running:")
        print("  docker-compose up -d qdrant")
        print("\nOr use --dry-run to preview content without Qdrant")
        sys.exit(1)
    
    print("Loading embedding model (this may take a while on first run)...")
    await embedding_service.initialize()
    
    print(f"Adding {args.source} source from {data_path}...")
    
    if args.source == "tatoeba":
        success = ingestion_service.add_tatoeba_source(data_path)
    elif args.source == "samanantar":
        success = ingestion_service.add_samanantar_source(data_path, max_items=args.max_items)
    elif args.source == "custom":
        success = ingestion_service.add_custom_source(
            data_path,
            source_name=args.name,
            license_info=args.license,
        )
    else:
        # Add all sources from subdirectories
        success = True
        for subdir in data_path.iterdir():
            if subdir.is_dir():
                if subdir.name == "tatoeba":
                    ingestion_service.add_tatoeba_source(subdir)
                elif subdir.name == "samanantar":
                    ingestion_service.add_samanantar_source(subdir, max_items=args.max_items)
                else:
                    ingestion_service.add_custom_source(subdir, source_name=subdir.name)
    
    if not success and args.source != "all":
        print("Error: Failed to add data source")
        sys.exit(1)
    
    print("Starting ingestion...")
    stats = await ingestion_service.ingest_all()
    
    print("\n=== Ingestion Complete ===")
    print(f"Total processed: {stats['total_processed']}")
    print(f"Total stored: {stats['total_stored']}")
    print(f"Errors: {stats['errors']}")
    
    for source, source_stats in stats["sources"].items():
        print(f"\n{source}:")
        print(f"  Processed: {source_stats['processed']}")
        print(f"  Stored: {source_stats['stored']}")
        print(f"  Errors: {source_stats['errors']}")
    
    # Get collection info
    info = await vector_db.get_collection_info()
    print(f"\nVector DB collection '{info['name']}': {info['points_count']} items")
    
    await vector_db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
