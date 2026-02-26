"""
Database migration script for Telugu AI Tutor.
Run this script to create tables and seed initial data.
"""
import asyncio
import asyncpg
import os
from pathlib import Path


async def run_migrations():
    """Run database migrations"""
    # Get database connection parameters from environment
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/telugu_tutor"
    )
    
    # Parse the URL
    url = database_url.replace("postgresql+asyncpg://", "")
    if "@" in url:
        credentials, host_part = url.split("@")
        user, password = credentials.split(":")
        host_db = host_part.split("/")
        host_port = host_db[0].split(":")
        host = host_port[0]
        port = int(host_port[1]) if len(host_port) > 1 else 5432
        database = host_db[1] if len(host_db) > 1 else "telugu_tutor"
    else:
        user = "postgres"
        password = "postgres"
        host = "localhost"
        port = 5432
        database = "telugu_tutor"

    print(f"Connecting to database: {host}:{port}/{database}")
    
    try:
        conn = await asyncpg.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
        )
    except asyncpg.InvalidCatalogNameError:
        # Database doesn't exist, create it
        print(f"Database '{database}' does not exist. Creating...")
        sys_conn = await asyncpg.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database="postgres",
        )
        await sys_conn.execute(f'CREATE DATABASE "{database}"')
        await sys_conn.close()
        
        conn = await asyncpg.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
        )

    # Read and execute schema
    schema_path = Path(__file__).parent / "schema.sql"
    print(f"Running schema from: {schema_path}")
    
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    
    await conn.execute(schema_sql)
    print("Schema created successfully!")

    # Read and execute seed data
    seed_path = Path(__file__).parent / "seed_data.sql"
    print(f"Running seed data from: {seed_path}")
    
    with open(seed_path, "r", encoding="utf-8") as f:
        seed_sql = f.read()
    
    try:
        await conn.execute(seed_sql)
        print("Seed data inserted successfully!")
    except asyncpg.UniqueViolationError:
        print("Seed data already exists, skipping...")

    await conn.close()
    print("Migration completed!")


if __name__ == "__main__":
    asyncio.run(run_migrations())
