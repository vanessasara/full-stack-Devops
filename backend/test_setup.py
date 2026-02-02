"""
Backend setup verification script
Run this after setup to verify all components are working
"""

import sys
import os
from importlib import import_module


def test_imports():
    """Test that all required packages can be imported"""
    print("Testing package imports...")

    required_packages = [
        "fastapi",
        "uvicorn",
        "asyncpg",
        "sentence_transformers",
        "pydantic",
        "dotenv",
        "httpx",
        "litellm",
    ]

    failed_imports = []

    for package in required_packages:
        try:
            import_module(package)
            print(f"  ✅ {package}")
        except ImportError as e:
            print(f"  ❌ {package}: {e}")
            failed_imports.append(package)

    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All required packages are installed")
        return True


def test_environment():
    """Test that environment variables are set"""
    print("\nTesting environment variables...")

    from dotenv import load_dotenv
    load_dotenv()

    required_vars = [
        "GEMINI_API_KEY",
        "DATABASE_URL",
    ]

    missing_vars = []

    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var} is set")
        else:
            print(f"  ⚠️  {var} is not set")
            missing_vars.append(var)

    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Edit .env file and add the required values")
        return False
    else:
        print("\n✅ All required environment variables are set")
        return True


def test_fastapi():
    """Test that FastAPI app can be created"""
    print("\nTesting FastAPI application...")

    try:
        from main import app
        print("  ✅ FastAPI app created successfully")
        print(f"  ✅ App title: {app.title}")
        print(f"  ✅ App version: {app.version}")
        return True
    except Exception as e:
        print(f"  ❌ Failed to create FastAPI app: {e}")
        return False


def test_database_module():
    """Test that database module can be imported"""
    print("\nTesting database module...")

    try:
        from database import (
            get_database_pool,
            enable_pgvector_extension,
            test_database_connection,
        )
        print("  ✅ Database module imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Failed to import database module: {e}")
        return False


async def test_database_connection():
    """Test actual database connection (async)"""
    print("\nTesting database connection...")

    try:
        from database import test_database_connection as test_conn

        success = await test_conn()

        if success:
            print("  ✅ Database connection successful")
            return True
        else:
            print("  ❌ Database connection failed")
            return False
    except Exception as e:
        print(f"  ❌ Database connection error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Sony Interior Backend Setup Verification")
    print("=" * 50)
    print()

    results = []

    # Test imports
    results.append(("Imports", test_imports()))

    # Test environment
    results.append(("Environment", test_environment()))

    # Test FastAPI
    results.append(("FastAPI", test_fastapi()))

    # Test database module
    results.append(("Database Module", test_database_module()))

    # Summary
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)

    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False

    print()

    if all_passed:
        print("🎉 All tests passed! Backend is ready to run.")
        print("\nNext steps:")
        print("1. Run './start.sh' to start the server")
        print("2. Visit http://localhost:8000/docs for API documentation")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
