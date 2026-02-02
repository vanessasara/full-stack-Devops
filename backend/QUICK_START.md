# Quick Start Guide

## First Time Setup

### 1. Run Setup Script

```bash
cd backend
./setup.sh
```

This will:
- Create Python virtual environment
- Install all dependencies
- Create .env file from template

### 2. Configure Environment

Edit `backend/.env` and add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=your_neon_postgres_url_here
```

**Get API Keys:**
- **Gemini API**: Visit https://aistudio.google.com/apikey
- **Neon Database**: Visit https://neon.tech and create a project

### 3. Verify Setup

```bash
python test_setup.py
```

All tests should pass.

### 4. Set Up Database (Phase 10)

```bash
# Run database migrations
python run_migrations.py

# Verify database is configured correctly
python verify_database.py
```

This creates all required tables and indexes.

### 5. Start Server

```bash
./start.sh
```

The API will be available at http://localhost:8000

## Daily Development

### Starting the Server

```bash
cd backend
./start.sh
```

### Viewing API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI.

### Stopping the Server

Press `Ctrl+C` in the terminal.

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── requirements.txt     # Python dependencies
├── database/           # Database operations
├── routers/            # API endpoints (Phase 14+)
├── services/           # Business logic (Phase 11+)
├── models/             # Data schemas (Phase 14+)
└── utils/              # Helper functions
```

## Common Commands

```bash
# Install new package
pip install package-name
pip freeze > requirements.txt

# Run with custom port
uvicorn main:app --reload --port 8080

# Check Python version
python --version

# Activate virtual environment (if needed)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

## Troubleshooting

### "Command not found: ./setup.sh"

```bash
chmod +x setup.sh start.sh
```

### "ModuleNotFoundError"

Make sure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Database Connection Failed

1. Check DATABASE_URL in .env file
2. Verify Neon database is running
3. Check network connection

### Port Already in Use

Change port in start.sh or run manually:
```bash
uvicorn main:app --reload --port 8001
```

## Next Phases

After Phase 9 is complete, continue with:

- **Phase 10**: Database schema implementation
- **Phase 11**: Embeddings and RAG
- **Phase 12**: MCP servers
- **Phase 13**: AI agent setup
- **Phase 14**: Chat endpoint

See `implementation-guide.md` in project root for details.
