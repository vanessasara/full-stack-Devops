"""
Database package initialization
"""

from .connection import (
    get_database_pool,
    close_database_pool,
    get_db,
    enable_pgvector_extension,
    test_database_connection,
    get_database_version,
)

from .operations import (
    # Chat sessions
    create_chat_session,
    get_chat_session,
    update_chat_session,
    # Chat messages
    insert_chat_message,
    get_chat_history,
    # Embeddings
    insert_embedding,
    batch_insert_embeddings,
    search_similar_embeddings,
    delete_embeddings_by_source,
    # Text selections
    insert_text_selection,
    get_session_selections,
)

__all__ = [
    # Connection
    "get_database_pool",
    "close_database_pool",
    "get_db",
    "enable_pgvector_extension",
    "test_database_connection",
    "get_database_version",
    # Chat sessions
    "create_chat_session",
    "get_chat_session",
    "update_chat_session",
    # Chat messages
    "insert_chat_message",
    "get_chat_history",
    # Embeddings
    "insert_embedding",
    "batch_insert_embeddings",
    "search_similar_embeddings",
    "delete_embeddings_by_source",
    # Text selections
    "insert_text_selection",
    "get_session_selections",
]
