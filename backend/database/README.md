# Database Documentation

## Overview

Sony Interior uses **Neon Serverless Postgres** with **pgvector** extension for storing chat history, vector embeddings, and user interactions.

## Schema

### Tables

#### 1. `chat_sessions`
Stores chat session information and metadata.

| Column | Type | Description |
|--------|------|-------------|
| session_id | UUID | Primary key, auto-generated |
| created_at | TIMESTAMP | Session creation time |
| updated_at | TIMESTAMP | Last activity time |
| user_agent | TEXT | Browser user agent |
| current_page | TEXT | Current page URL |
| metadata | JSONB | Additional session data |

**Indexes:**
- `idx_chat_sessions_created_at` - Time-based queries
- `idx_chat_sessions_updated_at` - Recent session queries

#### 2. `chat_messages`
Stores individual messages in conversations.

| Column | Type | Description |
|--------|------|-------------|
| message_id | UUID | Primary key, auto-generated |
| session_id | UUID | Foreign key to chat_sessions |
| role | VARCHAR(20) | Message role (user, assistant, system) |
| content | TEXT | Message content |
| created_at | TIMESTAMP | Message creation time |
| token_usage | INTEGER | Tokens used for this message |
| page_context | TEXT | Page URL when sent |
| metadata | JSONB | Additional message data |

**Indexes:**
- `idx_chat_messages_session_id` - Fast conversation retrieval
- `idx_chat_messages_role` - Filter by role

**Constraints:**
- Foreign key to `chat_sessions` with CASCADE delete
- Role check constraint (user, assistant, system)

#### 3. `document_embeddings`
Stores vector embeddings for RAG retrieval.

| Column | Type | Description |
|--------|------|-------------|
| embedding_id | UUID | Primary key, auto-generated |
| source_type | VARCHAR(50) | Type of source (product, page_content, faq, policy) |
| source_id | TEXT | Source identifier |
| content_chunk | TEXT | Text content |
| embedding | vector(384) | Vector embedding (384 dimensions) |
| metadata | JSONB | Additional metadata |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Last update time |

**Indexes:**
- `idx_document_embeddings_vector` - IVFFlat index for similarity search
- `idx_document_embeddings_source_type` - Filter by type
- `idx_document_embeddings_source_id` - Filter by ID
- `idx_document_embeddings_source` - Composite filter

**Constraints:**
- Source type check constraint (product, page_content, faq, policy)

#### 4. `user_text_selections`
Stores text selections made by users.

| Column | Type | Description |
|--------|------|-------------|
| selection_id | UUID | Primary key, auto-generated |
| session_id | UUID | Foreign key to chat_sessions |
| selected_text | TEXT | Text selected by user |
| page_url | TEXT | URL where selection was made |
| created_at | TIMESTAMP | Selection time |
| embedding | vector(384) | Optional embedding of text |
| metadata | JSONB | Additional data |

**Indexes:**
- `idx_user_text_selections_session_id` - Session queries
- `idx_user_text_selections_page_url` - Page queries

**Constraints:**
- Foreign key to `chat_sessions` with CASCADE delete

## Running Migrations

### Initial Setup

1. Ensure DATABASE_URL is set in `.env`:
   ```bash
   DATABASE_URL=postgresql://username:password@host/database
   ```

2. Run migrations:
   ```bash
   cd backend
   python run_migrations.py
   ```

3. Run migrations with tests:
   ```bash
   python run_migrations.py --test
   ```

### What Migrations Do

The initial migration (`001_initial_schema.sql`) performs:
- ✅ Enables pgvector extension
- ✅ Creates all tables
- ✅ Creates indexes for performance
- ✅ Sets up foreign key constraints
- ✅ Creates triggers for auto-updating timestamps

## Using Database Operations

### Import Operations

```python
from database import (
    create_chat_session,
    insert_chat_message,
    get_chat_history,
    insert_embedding,
    search_similar_embeddings,
)
```

### Chat Session Operations

**Create Session:**
```python
session_id = await create_chat_session(
    user_agent="Mozilla/5.0...",
    current_page="/products",
    metadata={"source": "widget"}
)
```

**Get Session:**
```python
session = await get_chat_session(session_id)
```

**Update Session:**
```python
await update_chat_session(
    session_id=session_id,
    current_page="/about",
    metadata={"last_question": "shipping info"}
)
```

### Chat Message Operations

**Insert Message:**
```python
message_id = await insert_chat_message(
    session_id=session_id,
    role="user",
    content="What sofas are available?",
    page_context="/products"
)
```

**Get Chat History:**
```python
messages = await get_chat_history(
    session_id=session_id,
    limit=50
)
```

### Embedding Operations

**Insert Embedding:**
```python
embedding_id = await insert_embedding(
    source_type="product",
    source_id="vintage-sofa-123",
    content_chunk="Vintage leather sofa...",
    embedding=[0.1, 0.2, ...],  # 384 dimensions
    metadata={"category": "sofas"}
)
```

**Batch Insert:**
```python
embeddings_data = [
    {
        "source_type": "product",
        "source_id": "sofa-1",
        "content_chunk": "Description...",
        "embedding": [0.1, ...],
        "metadata": {}
    },
    # ... more embeddings
]

embedding_ids = await batch_insert_embeddings(embeddings_data)
```

**Similarity Search:**
```python
results = await search_similar_embeddings(
    query_embedding=[0.1, 0.2, ...],
    source_type="product",  # Optional filter
    limit=5,
    similarity_threshold=0.7
)

for result in results:
    print(f"Content: {result['content_chunk']}")
    print(f"Similarity: {result['similarity']}")
```

**Delete Embeddings:**
```python
count = await delete_embeddings_by_source(
    source_type="product",
    source_id="old-product-123"
)
```

### Text Selection Operations

**Insert Selection:**
```python
selection_id = await insert_text_selection(
    session_id=session_id,
    selected_text="free shipping on orders over $500",
    page_url="/products/sofa-123",
    embedding=[0.1, ...]  # Optional
)
```

**Get Session Selections:**
```python
selections = await get_session_selections(
    session_id=session_id,
    limit=10
)
```

## Vector Similarity Search

### Understanding Similarity Scores

Similarity scores range from 0 to 1:
- **0.9 - 1.0**: Nearly identical
- **0.7 - 0.9**: Very similar
- **0.5 - 0.7**: Somewhat similar
- **0.0 - 0.5**: Not similar

### Query Example

```python
# Generate embedding for user question
question = "Show me modern leather sofas"
query_embedding = generate_embedding(question)  # Phase 11

# Search for relevant products
results = await search_similar_embeddings(
    query_embedding=query_embedding,
    source_type="product",
    limit=5,
    similarity_threshold=0.6
)

# Results are ordered by similarity (highest first)
```

## Performance Considerations

### Indexes

- **IVFFlat index** on embeddings enables fast approximate nearest neighbor search
- Time complexity: O(log n) for similarity search
- Trade-off: Slightly less accurate than exact search, much faster

### Optimization Tips

1. **Limit results**: Use reasonable `limit` values (5-10)
2. **Filter by source_type**: Reduces search space
3. **Batch operations**: Use `batch_insert_embeddings` for multiple inserts
4. **Connection pooling**: Already configured in `connection.py`
5. **Prune old data**: Delete old chat sessions periodically

### Monitoring

Check index usage:
```sql
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

## Troubleshooting

### pgvector Extension Not Found

```bash
# Connect to database and run:
CREATE EXTENSION IF NOT EXISTS vector;
```

### Migration Fails

1. Check DATABASE_URL is correct
2. Ensure database is accessible
3. Check user has CREATE permissions
4. Review error logs in console

### Slow Similarity Search

1. Verify IVFFlat index exists:
   ```sql
   \d document_embeddings
   ```
2. Rebuild index if needed:
   ```sql
   REINDEX INDEX idx_document_embeddings_vector;
   ```
3. Increase lists parameter for larger datasets

### Connection Pool Exhausted

Increase pool size in `connection.py`:
```python
_pool = await asyncpg.create_pool(
    database_url,
    min_size=5,  # Increase from 2
    max_size=20,  # Increase from 10
)
```

## Next Steps

After Phase 10, you'll use this database for:
- **Phase 11**: Store product and content embeddings
- **Phase 13**: Save chat conversations
- **Phase 14**: Provide RAG context to AI agent
