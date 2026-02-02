# Sony Interior Backend API

FastAPI backend for AI-powered furniture consultation with RAG capabilities.

## Features

- **AI Agent**: OpenAI Agent SDK routed through LiteLLM to Google Gemini
- **RAG System**: Vector embeddings with pgvector for intelligent product search
- **MCP Integration**: Real-time data access through Model Context Protocol servers
- **Chat API**: Streaming responses with conversation history
- **Embeddings**: Sentence transformers for semantic search

## Prerequisites

- Python 3.11 or higher
- PostgreSQL with pgvector extension (Neon recommended)
- Google Gemini API key

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

- `GEMINI_API_KEY`: Get from https://aistudio.google.com/apikey
- `DATABASE_URL`: Your Neon Postgres connection string
- Other variables as needed

### 4. Run Development Server

```bash
# Using Python directly
python main.py

# Or using uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── database/              # Database operations
│   ├── __init__.py
│   └── connection.py      # Connection pooling and pgvector setup
├── routers/               # API route handlers
│   └── __init__.py
├── services/              # Business logic
│   └── __init__.py
├── models/                # Pydantic schemas
│   └── __init__.py
└── utils/                 # Helper functions
    └── __init__.py
```

## API Endpoints

### Current Endpoints

- `GET /` - API status and information
- `GET /health` - Health check with component status

### Upcoming Endpoints (Later Phases)

- `POST /api/chat` - Send chat messages to AI agent
- `GET /api/quick-questions` - Get contextual quick questions
- `POST /api/embeddings` - Generate embeddings for content

## Development Workflow

### Testing Database Connection

The `/health` endpoint shows database connection status once initialized.

### Viewing API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.

### Running with Auto-reload

The server automatically reloads when you make changes to Python files.

## Database Setup (Phase 10)

After initial backend setup, you need to set up the database schema:

### 1. Get Neon Database URL

1. Visit https://neon.tech
2. Create a new project
3. Copy the connection string (starts with `postgresql://`)
4. Add to `.env` as `DATABASE_URL`

### 2. Run Migrations

```bash
# Apply database schema
python run_migrations.py

# Run migrations with tests
python run_migrations.py --test

# Verify database setup
python verify_database.py
```

This creates:
- 4 tables (chat_sessions, chat_messages, document_embeddings, user_text_selections)
- pgvector extension for vector similarity search
- Indexes for performance
- Foreign key constraints

See `database/README.md` for complete schema documentation.

## Phases

This backend is built in phases according to the implementation guide:

- **Phase 9** ✅ - Backend setup with FastAPI, database connection
- **Phase 10** ✅ - Database schema implementation
- **Phase 11** - Embeddings and RAG implementation
- **Phase 12** - MCP server development
- **Phase 13** - OpenAI Agent SDK with LiteLLM
- **Phase 14** - Chat endpoint implementation
- **Phase 15** - Quick questions feature

## Troubleshooting

### ModuleNotFoundError

Make sure your virtual environment is activated and all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Database Connection Errors

Verify your `DATABASE_URL` is correct and the database is accessible.

### CORS Errors

Check that `NEXT_PUBLIC_API_URL` matches your Next.js frontend URL.

## Next Steps

See `implementation-guide.md` in the project root for detailed instructions on:
- Phase 10: Database schema setup
- Phase 11: Implementing embeddings
- Phase 12: Building MCP servers
- Phase 13: Setting up the AI agent
