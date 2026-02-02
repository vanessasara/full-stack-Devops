"""
Database operations module
Helper functions for common database operations
"""

import asyncpg
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging
from uuid import UUID
import json

from .connection import get_database_pool

logger = logging.getLogger(__name__)


# =====================================================
# Chat Session Operations
# =====================================================

async def create_chat_session(
    user_agent: Optional[str] = None,
    current_page: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create a new chat session

    Args:
        user_agent: User agent string from browser
        current_page: Current page URL
        metadata: Additional session metadata

    Returns:
        session_id as string
    """
    pool = await get_database_pool()

    metadata_json = json.dumps(metadata) if metadata else '{}'

    async with pool.acquire() as conn:
        try:
            session_id = await conn.fetchval(
                """
                INSERT INTO chat_sessions (user_agent, current_page, metadata)
                VALUES ($1, $2, $3)
                RETURNING session_id
                """,
                user_agent,
                current_page,
                metadata_json
            )

            logger.info(f"Created chat session: {session_id}")
            return str(session_id)

        except Exception as e:
            logger.error(f"Error creating chat session: {e}")
            raise


async def get_chat_session(session_id: str) -> Optional[Dict[str, Any]]:
    """
    Get chat session by ID

    Args:
        session_id: Session UUID as string

    Returns:
        Session data as dict or None if not found
    """
    pool = await get_database_pool()

    async with pool.acquire() as conn:
        try:
            row = await conn.fetchrow(
                """
                SELECT session_id, created_at, updated_at, user_agent, current_page, metadata
                FROM chat_sessions
                WHERE session_id = $1
                """,
                UUID(session_id)
            )

            if row:
                return dict(row)
            return None

        except Exception as e:
            logger.error(f"Error getting chat session {session_id}: {e}")
            raise


async def update_chat_session(
    session_id: str,
    current_page: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Update chat session information

    Args:
        session_id: Session UUID as string
        current_page: Updated current page URL
        metadata: Updated metadata (will be merged with existing)

    Returns:
        True if update successful, False otherwise
    """
    pool = await get_database_pool()

    async with pool.acquire() as conn:
        try:
            # Build update query dynamically based on provided parameters
            updates = []
            params = [UUID(session_id)]
            param_count = 2

            if current_page is not None:
                updates.append(f"current_page = ${param_count}")
                params.append(current_page)
                param_count += 1

            if metadata is not None:
                updates.append(f"metadata = metadata || ${param_count}::jsonb")
                params.append(json.dumps(metadata))
                param_count += 1

            if not updates:
                return False

            query = f"""
                UPDATE chat_sessions
                SET {', '.join(updates)}
                WHERE session_id = $1
                RETURNING session_id
            """

            result = await conn.fetchval(query, *params)
            return result is not None

        except Exception as e:
            logger.error(f"Error updating chat session {session_id}: {e}")
            raise


# =====================================================
# Chat Message Operations
# =====================================================

async def insert_chat_message(
    session_id: str,
    role: str,
    content: str,
    token_usage: int = 0,
    page_context: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Insert a chat message

    Args:
        session_id: Session UUID as string
        role: Message role (user, assistant, system)
        content: Message content
        token_usage: Number of tokens used
        page_context: Page context when message was sent
        metadata: Additional message metadata

    Returns:
        message_id as string
    """
    pool = await get_database_pool()

    metadata_json = json.dumps(metadata) if metadata else '{}'

    async with pool.acquire() as conn:
        try:
            message_id = await conn.fetchval(
                """
                INSERT INTO chat_messages
                (session_id, role, content, token_usage, page_context, metadata)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING message_id
                """,
                UUID(session_id),
                role,
                content,
                token_usage,
                page_context,
                metadata_json
            )

            # Update session's updated_at timestamp
            await conn.execute(
                "UPDATE chat_sessions SET updated_at = NOW() WHERE session_id = $1",
                UUID(session_id)
            )

            logger.debug(f"Inserted chat message {message_id} for session {session_id}")
            return str(message_id)

        except Exception as e:
            logger.error(f"Error inserting chat message: {e}")
            raise


async def get_chat_history(
    session_id: str,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Get chat history for a session

    Args:
        session_id: Session UUID as string
        limit: Maximum number of messages to return
        offset: Number of messages to skip

    Returns:
        List of message dicts ordered by creation time
    """
    pool = await get_database_pool()

    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch(
                """
                SELECT message_id, session_id, role, content, created_at,
                       token_usage, page_context, metadata
                FROM chat_messages
                WHERE session_id = $1
                ORDER BY created_at ASC
                LIMIT $2 OFFSET $3
                """,
                UUID(session_id),
                limit,
                offset
            )

            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Error getting chat history for session {session_id}: {e}")
            raise


# =====================================================
# Document Embedding Operations
# =====================================================

async def insert_embedding(
    source_type: str,
    source_id: str,
    content_chunk: str,
    embedding: List[float],
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Insert a document embedding

    Args:
        source_type: Type of source (product, page_content, faq, policy)
        source_id: Identifier for the source
        content_chunk: Text content
        embedding: Vector embedding (384 dimensions)
        metadata: Additional metadata

    Returns:
        embedding_id as string
    """
    pool = await get_database_pool()

    metadata_json = json.dumps(metadata) if metadata else '{}'

    async with pool.acquire() as conn:
        try:
            embedding_id = await conn.fetchval(
                """
                INSERT INTO document_embeddings
                (source_type, source_id, content_chunk, embedding, metadata)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING embedding_id
                """,
                source_type,
                source_id,
                content_chunk,
                embedding,
                metadata_json
            )

            logger.debug(f"Inserted embedding {embedding_id} for {source_type}/{source_id}")
            return str(embedding_id)

        except Exception as e:
            logger.error(f"Error inserting embedding: {e}")
            raise


async def batch_insert_embeddings(
    embeddings_data: List[Dict[str, Any]]
) -> List[str]:
    """
    Batch insert multiple embeddings

    Args:
        embeddings_data: List of dicts with keys: source_type, source_id,
                        content_chunk, embedding, metadata (optional)

    Returns:
        List of embedding_ids as strings
    """
    pool = await get_database_pool()

    async with pool.acquire() as conn:
        try:
            embedding_ids = []

            async with conn.transaction():
                for data in embeddings_data:
                    metadata_json = json.dumps(data.get('metadata', {}))

                    embedding_id = await conn.fetchval(
                        """
                        INSERT INTO document_embeddings
                        (source_type, source_id, content_chunk, embedding, metadata)
                        VALUES ($1, $2, $3, $4, $5)
                        RETURNING embedding_id
                        """,
                        data['source_type'],
                        data['source_id'],
                        data['content_chunk'],
                        data['embedding'],
                        metadata_json
                    )

                    embedding_ids.append(str(embedding_id))

            logger.info(f"Batch inserted {len(embedding_ids)} embeddings")
            return embedding_ids

        except Exception as e:
            logger.error(f"Error batch inserting embeddings: {e}")
            raise


async def search_similar_embeddings(
    query_embedding: List[float],
    source_type: Optional[str] = None,
    limit: int = 5,
    similarity_threshold: float = 0.0
) -> List[Dict[str, Any]]:
    """
    Search for similar embeddings using cosine similarity

    Args:
        query_embedding: Query vector (384 dimensions)
        source_type: Optional filter by source type
        limit: Maximum number of results to return
        similarity_threshold: Minimum similarity score (0-1)

    Returns:
        List of similar documents with similarity scores
    """
    pool = await get_database_pool()

    async with pool.acquire() as conn:
        try:
            # Build query based on source_type filter
            if source_type:
                query = """
                    SELECT
                        embedding_id,
                        source_type,
                        source_id,
                        content_chunk,
                        metadata,
                        1 - (embedding <=> $1) as similarity
                    FROM document_embeddings
                    WHERE source_type = $2
                    ORDER BY embedding <=> $1
                    LIMIT $3
                """
                params = [query_embedding, source_type, limit]
            else:
                query = """
                    SELECT
                        embedding_id,
                        source_type,
                        source_id,
                        content_chunk,
                        metadata,
                        1 - (embedding <=> $1) as similarity
                    FROM document_embeddings
                    ORDER BY embedding <=> $1
                    LIMIT $2
                """
                params = [query_embedding, limit]

            rows = await conn.fetch(query, *params)

            # Filter by similarity threshold
            results = [
                dict(row) for row in rows
                if row['similarity'] >= similarity_threshold
            ]

            logger.debug(f"Found {len(results)} similar embeddings")
            return results

        except Exception as e:
            logger.error(f"Error searching similar embeddings: {e}")
            raise


async def delete_embeddings_by_source(
    source_type: str,
    source_id: str
) -> int:
    """
    Delete all embeddings for a specific source

    Args:
        source_type: Type of source
        source_id: Source identifier

    Returns:
        Number of embeddings deleted
    """
    pool = await get_database_pool()

    async with pool.acquire() as conn:
        try:
            result = await conn.execute(
                """
                DELETE FROM document_embeddings
                WHERE source_type = $1 AND source_id = $2
                """,
                source_type,
                source_id
            )

            # Extract number from result string like "DELETE 5"
            count = int(result.split()[-1])
            logger.info(f"Deleted {count} embeddings for {source_type}/{source_id}")
            return count

        except Exception as e:
            logger.error(f"Error deleting embeddings: {e}")
            raise


# =====================================================
# User Text Selection Operations
# =====================================================

async def insert_text_selection(
    session_id: str,
    selected_text: str,
    page_url: str,
    embedding: Optional[List[float]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Insert a user text selection

    Args:
        session_id: Session UUID as string
        selected_text: Text selected by user
        page_url: URL where selection was made
        embedding: Optional embedding of selected text
        metadata: Additional metadata

    Returns:
        selection_id as string
    """
    pool = await get_database_pool()

    metadata_json = json.dumps(metadata) if metadata else '{}'

    async with pool.acquire() as conn:
        try:
            selection_id = await conn.fetchval(
                """
                INSERT INTO user_text_selections
                (session_id, selected_text, page_url, embedding, metadata)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING selection_id
                """,
                UUID(session_id),
                selected_text,
                page_url,
                embedding,
                metadata_json
            )

            logger.debug(f"Inserted text selection {selection_id}")
            return str(selection_id)

        except Exception as e:
            logger.error(f"Error inserting text selection: {e}")
            raise


async def get_session_selections(
    session_id: str,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Get text selections for a session

    Args:
        session_id: Session UUID as string
        limit: Maximum number of selections to return

    Returns:
        List of selection dicts
    """
    pool = await get_database_pool()

    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch(
                """
                SELECT selection_id, session_id, selected_text, page_url,
                       created_at, metadata
                FROM user_text_selections
                WHERE session_id = $1
                ORDER BY created_at DESC
                LIMIT $2
                """,
                UUID(session_id),
                limit
            )

            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Error getting text selections for session {session_id}: {e}")
            raise
