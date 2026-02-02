"""
Database verification script
Checks if the database schema is properly set up
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv
import sys

load_dotenv()


async def verify_database():
    """
    Verify database setup
    """
    print("=" * 60)
    print("Sony Interior - Database Verification")
    print("=" * 60)

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("\n❌ DATABASE_URL not set in .env file")
        sys.exit(1)

    try:
        # Connect to database
        print("\n1. Testing database connection...")
        conn = await asyncpg.connect(database_url)
        print("   ✅ Connected successfully")

        # Check PostgreSQL version
        print("\n2. Checking PostgreSQL version...")
        version = await conn.fetchval("SELECT version()")
        print(f"   ✅ {version.split(',')[0]}")

        # Check pgvector extension
        print("\n3. Checking pgvector extension...")
        ext = await conn.fetchrow(
            "SELECT * FROM pg_extension WHERE extname = 'vector'"
        )
        if ext:
            print(f"   ✅ pgvector extension enabled (version {ext['extversion']})")
        else:
            print("   ❌ pgvector extension not found")
            print("   Run: python run_migrations.py")

        # Check required tables
        print("\n4. Checking required tables...")
        required_tables = [
            'chat_sessions',
            'chat_messages',
            'document_embeddings',
            'user_text_selections'
        ]

        tables = await conn.fetch("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
        """)

        existing_tables = [t['tablename'] for t in tables]

        all_tables_exist = True
        for table in required_tables:
            if table in existing_tables:
                print(f"   ✅ {table}")
            else:
                print(f"   ❌ {table} - MISSING")
                all_tables_exist = False

        if not all_tables_exist:
            print("\n   ⚠️  Some tables are missing. Run migrations:")
            print("   python run_migrations.py")

        # Check indexes
        print("\n5. Checking indexes...")
        indexes = await conn.fetch("""
            SELECT indexname, tablename
            FROM pg_indexes
            WHERE schemaname = 'public'
            AND indexname LIKE 'idx_%'
        """)

        if len(indexes) >= 8:  # Minimum expected indexes
            print(f"   ✅ Found {len(indexes)} indexes")
        else:
            print(f"   ⚠️  Expected at least 8 indexes, found {len(indexes)}")

        # Check vector index specifically
        vector_idx = await conn.fetch("""
            SELECT indexname
            FROM pg_indexes
            WHERE indexname = 'idx_document_embeddings_vector'
        """)

        if vector_idx:
            print("   ✅ Vector similarity search index exists")
        else:
            print("   ❌ Vector similarity search index missing")

        # Test table structures
        print("\n6. Verifying table structures...")

        # Chat sessions
        sessions_cols = await conn.fetch("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'chat_sessions'
        """)
        if len(sessions_cols) >= 6:
            print("   ✅ chat_sessions structure correct")
        else:
            print("   ❌ chat_sessions structure incorrect")

        # Document embeddings
        embeddings_cols = await conn.fetch("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'document_embeddings'
        """)

        has_vector = any(col['data_type'] == 'USER-DEFINED' for col in embeddings_cols)
        if has_vector:
            print("   ✅ document_embeddings has vector column")
        else:
            print("   ❌ document_embeddings missing vector column")

        # Test basic operations
        print("\n7. Testing basic operations...")

        # Test insert and delete
        try:
            # Insert test session
            test_session = await conn.fetchval("""
                INSERT INTO chat_sessions (user_agent, current_page)
                VALUES ('Test', '/test')
                RETURNING session_id
            """)
            print("   ✅ Insert operation works")

            # Delete test session
            await conn.execute("""
                DELETE FROM chat_sessions WHERE session_id = $1
            """, test_session)
            print("   ✅ Delete operation works")

        except Exception as e:
            print(f"   ❌ Basic operations failed: {e}")

        await conn.close()

        # Summary
        print("\n" + "=" * 60)
        if all_tables_exist and ext and vector_idx:
            print("✅ Database is properly configured!")
            print("\nYou can now:")
            print("1. Start the backend: ./start.sh")
            print("2. Begin Phase 11: Embeddings implementation")
            print("=" * 60)
            sys.exit(0)
        else:
            print("⚠️  Database needs configuration")
            print("\nPlease run:")
            print("  python run_migrations.py")
            print("=" * 60)
            sys.exit(1)

    except asyncpg.PostgresError as e:
        print(f"\n❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(verify_database())
