-- Sony Interior Database Schema
-- Migration 001: Initial schema with pgvector support
-- Created: 2026-02-02

-- Enable pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- =====================================================
-- Chat Sessions Table
-- Stores chat session information and metadata
-- =====================================================
CREATE TABLE IF NOT EXISTS chat_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    user_agent TEXT,
    current_page TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Index for time-based queries
CREATE INDEX IF NOT EXISTS idx_chat_sessions_created_at
ON chat_sessions(created_at DESC);

-- Index for updated_at to find recent sessions
CREATE INDEX IF NOT EXISTS idx_chat_sessions_updated_at
ON chat_sessions(updated_at DESC);

-- =====================================================
-- Chat Messages Table
-- Stores individual messages in conversations
-- =====================================================
CREATE TABLE IF NOT EXISTS chat_messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    token_usage INTEGER DEFAULT 0,
    page_context TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Foreign key constraint
    CONSTRAINT fk_session
        FOREIGN KEY (session_id)
        REFERENCES chat_sessions(session_id)
        ON DELETE CASCADE
);

-- Index for fast conversation retrieval
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id
ON chat_messages(session_id, created_at);

-- Index for role filtering
CREATE INDEX IF NOT EXISTS idx_chat_messages_role
ON chat_messages(role);

-- =====================================================
-- Document Embeddings Table
-- Stores vector embeddings for RAG retrieval
-- =====================================================
CREATE TABLE IF NOT EXISTS document_embeddings (
    embedding_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type VARCHAR(50) NOT NULL CHECK (source_type IN ('product', 'page_content', 'faq', 'policy')),
    source_id TEXT NOT NULL,
    content_chunk TEXT NOT NULL,
    embedding vector(384) NOT NULL,  -- 384 dimensions for all-MiniLM-L6-v2
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Vector similarity search index using IVFFlat
-- Lists parameter (100) is good for datasets with 10k-1M vectors
CREATE INDEX IF NOT EXISTS idx_document_embeddings_vector
ON document_embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Index for filtering by source type
CREATE INDEX IF NOT EXISTS idx_document_embeddings_source_type
ON document_embeddings(source_type);

-- Index for filtering by source ID
CREATE INDEX IF NOT EXISTS idx_document_embeddings_source_id
ON document_embeddings(source_id);

-- Composite index for source filtering
CREATE INDEX IF NOT EXISTS idx_document_embeddings_source
ON document_embeddings(source_type, source_id);

-- =====================================================
-- User Text Selections Table
-- Stores text selections made by users for context
-- =====================================================
CREATE TABLE IF NOT EXISTS user_text_selections (
    selection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL,
    selected_text TEXT NOT NULL,
    page_url TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    embedding vector(384),  -- Optional embedding of selected text
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Foreign key constraint
    CONSTRAINT fk_selection_session
        FOREIGN KEY (session_id)
        REFERENCES chat_sessions(session_id)
        ON DELETE CASCADE
);

-- Index for session-based queries
CREATE INDEX IF NOT EXISTS idx_user_text_selections_session_id
ON user_text_selections(session_id, created_at);

-- Index for page-based queries
CREATE INDEX IF NOT EXISTS idx_user_text_selections_page_url
ON user_text_selections(page_url);

-- =====================================================
-- Helper Functions
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for chat_sessions updated_at
CREATE TRIGGER update_chat_sessions_updated_at
    BEFORE UPDATE ON chat_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for document_embeddings updated_at
CREATE TRIGGER update_document_embeddings_updated_at
    BEFORE UPDATE ON document_embeddings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- Verification Queries
-- =====================================================

-- Verify pgvector extension
-- SELECT * FROM pg_extension WHERE extname = 'vector';

-- List all tables
-- SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Check table structures
-- \d chat_sessions
-- \d chat_messages
-- \d document_embeddings
-- \d user_text_selections

-- Verify indexes
-- SELECT indexname, tablename FROM pg_indexes WHERE schemaname = 'public';
