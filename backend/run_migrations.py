"""
Database migration runner
Applies SQL migrations to the database
"""

import asyncio
import asyncpg
import os
from pathlib import Path
import sys
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def run_migration(migration_file: Path, conn: asyncpg.Connection):
    """
    Run a single migration file

    Args:
        migration_file: Path to SQL migration file
        conn: Database connection
    """
    logger.info(f"Running migration: {migration_file.name}")

    try:
        # Read migration SQL
        with open(migration_file, 'r') as f:
            sql = f.read()

        # Execute migration
        await conn.execute(sql)

        logger.info(f"✅ Successfully applied: {migration_file.name}")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to apply {migration_file.name}: {e}")
        return False


async def run_all_migrations():
    """
    Run all pending migrations in order
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        logger.error("❌ DATABASE_URL environment variable is not set")
        logger.error("Please set DATABASE_URL in your .env file")
        sys.exit(1)

    logger.info("Starting database migrations...")
    logger.info(f"Database: {database_url.split('@')[1] if '@' in database_url else 'localhost'}")

    try:
        # Connect to database
        conn = await asyncpg.connect(database_url)
        logger.info("✅ Connected to database")

        # Find all migration files
        migrations_dir = Path(__file__).parent / "database" / "migrations"

        if not migrations_dir.exists():
            logger.error(f"❌ Migrations directory not found: {migrations_dir}")
            sys.exit(1)

        migration_files = sorted(migrations_dir.glob("*.sql"))

        if not migration_files:
            logger.warning("⚠️  No migration files found")
            await conn.close()
            return

        logger.info(f"Found {len(migration_files)} migration file(s)")

        # Run each migration
        success_count = 0
        for migration_file in migration_files:
            if await run_migration(migration_file, conn):
                success_count += 1
            else:
                logger.error("❌ Migration failed, stopping")
                break

        # Verify tables were created
        logger.info("\nVerifying database schema...")

        tables = await conn.fetch("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename
        """)

        logger.info(f"\nCreated tables ({len(tables)}):")
        for table in tables:
            logger.info(f"  ✅ {table['tablename']}")

        # Verify pgvector extension
        extensions = await conn.fetch("""
            SELECT extname, extversion
            FROM pg_extension
            WHERE extname = 'vector'
        """)

        if extensions:
            logger.info(f"\n✅ pgvector extension enabled (version {extensions[0]['extversion']})")
        else:
            logger.warning("\n⚠️  pgvector extension not found")

        # Verify indexes
        indexes = await conn.fetch("""
            SELECT indexname, tablename
            FROM pg_indexes
            WHERE schemaname = 'public'
            AND indexname LIKE 'idx_%'
            ORDER BY tablename, indexname
        """)

        logger.info(f"\nCreated indexes ({len(indexes)}):")
        for idx in indexes:
            logger.info(f"  ✅ {idx['indexname']} on {idx['tablename']}")

        await conn.close()

        logger.info(f"\n{'='*60}")
        logger.info(f"Migration complete!")
        logger.info(f"Applied {success_count}/{len(migration_files)} migration(s)")
        logger.info(f"{'='*60}")

    except asyncpg.PostgresError as e:
        logger.error(f"❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)


async def test_database():
    """
    Test database by inserting and querying sample data
    """
    from database import (
        create_chat_session,
        insert_chat_message,
        get_chat_history,
        insert_embedding,
        search_similar_embeddings,
    )

    logger.info("\n" + "="*60)
    logger.info("Testing database operations...")
    logger.info("="*60)

    try:
        # Test chat session
        logger.info("\n1. Testing chat session creation...")
        session_id = await create_chat_session(
            user_agent="Test Agent",
            current_page="/test",
            metadata={"test": True}
        )
        logger.info(f"✅ Created session: {session_id}")

        # Test chat message
        logger.info("\n2. Testing chat message insertion...")
        message_id = await insert_chat_message(
            session_id=session_id,
            role="user",
            content="Test message",
            token_usage=10
        )
        logger.info(f"✅ Created message: {message_id}")

        # Test chat history retrieval
        logger.info("\n3. Testing chat history retrieval...")
        history = await get_chat_history(session_id)
        logger.info(f"✅ Retrieved {len(history)} message(s)")

        # Test embedding insertion
        logger.info("\n4. Testing embedding insertion...")
        test_embedding = [0.1] * 384  # 384-dimensional vector
        embedding_id = await insert_embedding(
            source_type="product",
            source_id="test-product",
            content_chunk="Test product description",
            embedding=test_embedding,
            metadata={"test": True}
        )
        logger.info(f"✅ Created embedding: {embedding_id}")

        # Test similarity search
        logger.info("\n5. Testing similarity search...")
        query_embedding = [0.1] * 384
        results = await search_similar_embeddings(
            query_embedding=query_embedding,
            limit=5
        )
        logger.info(f"✅ Found {len(results)} similar embedding(s)")

        logger.info("\n" + "="*60)
        logger.info("All database tests passed! ✅")
        logger.info("="*60)

    except Exception as e:
        logger.error(f"❌ Database test failed: {e}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run database migrations")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run tests after migrations"
    )

    args = parser.parse_args()

    # Run migrations
    asyncio.run(run_all_migrations())

    # Run tests if requested
    if args.test:
        asyncio.run(test_database())
