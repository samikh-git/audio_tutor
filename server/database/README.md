# Audio Tutor Database Documentation

## Overview
The Audio Tutor application uses SQLite to store conversation history and LangChain checkpoints. This document explains the database organization and how to manage it.

## Database Files
- `conversation_history.db` - Main database file for conversation history
- `conversation_history.db-shm` - Shared memory file (WAL mode)
- `conversation_history.db-wal` - Write-Ahead Log file (WAL mode)
- `vector_database.db` - Vector database for semantic search and retrieval

## Database Schema

### conversation_history Table
Stores all conversation sessions between users and the AI tutor.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key, auto-increment |
| user_id | TEXT | Unique identifier for the user |
| session_date | DATE | Date of the conversation session |
| transcript | TEXT | Full conversation transcript |
| created_at | TIMESTAMP | When the record was created |
| updated_at | TIMESTAMP | When the record was last updated |

### LangChain Tables
- `checkpoints` - Stores conversation checkpoints for LangChain
- `writes` - Stores write operations for LangChain

## Vector Database

### Overview
The vector database uses **Milvus** (via `langchain-milvus`) to store conversation embeddings for semantic search and retrieval. This enables the AI tutor to find relevant conversation history when analyzing student performance.

### Vector Database Schema
The vector database stores documents with the following structure:
- **Content**: Full conversation transcripts
- **Metadata**: 
  - `namespace`: User ID for partitioning
  - `pk`: Primary key (UUID)
- **Embeddings**: Generated using Google's Gemini embedding model

### Vector Database Configuration
```python
# Configuration in analyzer_tutor.py
vector_store = Milvus(
    embedding_function=embeddings,  # GoogleGenerativeAIEmbeddings
    connection_args={"uri": "../database/vector_database.db"},
    index_params={"index_type": "FLAT", "metric_type": "L2"},
    partition_key_field="namespace",
)
```

### Vector Database Operations

#### Adding Documents
```python
from analyzer_tutor import add_document

# Add a conversation to the vector database
add_document(
    page_content="Full conversation transcript...",
    user_id="user_123"
)
```

#### Retrieving Documents
```python
from analyzer_tutor import vector_store

# Search for similar conversations
results = vector_store.similarity_search(
    query="grammar mistakes",
    k=5,  # Number of results
    search_kwargs={"expr": 'namespace == "user_123"'}
)
```

#### Removing Documents
```python
from analyzer_tutor import remove_document

# Remove a specific document by UUID
remove_document("document-uuid-here")
```

### Vector Database Integration

#### In the Analyzer Agent
The vector database is used by the language tutor analyzer to:
1. **Retrieve conversation history** for specific users
2. **Find similar patterns** in language use
3. **Provide context-aware feedback** based on historical data
4. **Track progress** over time

#### Retrieval Tool
```python
@tool
def retrieve(query: str, user_id: str):
    """Retrieve conversation history for a specific user_id."""
    retrieved_docs = vector_store.similarity_search(
        query, 
        k=5, 
        search_kwargs={"expr": f'namespace == "{user_id}"'}
    )
    # Process and return results
```

### Vector Database Management

#### Automatic Population
The vector database is automatically populated when conversations are saved:
```python
# In app.py - automatically adds to vector database
conversation_id = db_manager.save_conversation(user_id, today, long_transcript)
add_document(long_transcript, user_id)  # Adds to vector database
```

#### Manual Management
```bash
# Check vector database size
ls -la vector_database.db

# Backup vector database
cp vector_database.db vector_database_backup.db
```

### Vector Database Performance

#### Index Configuration
- **Index Type**: FLAT (exact search, good for small datasets)
- **Metric Type**: L2 (Euclidean distance)
- **Partitioning**: By user_id (namespace)

## Database Architecture

### Dual Database System
The Audio Tutor application uses a dual database architecture:

1. **SQLite Database** (`conversation_history.db`)
   - Stores structured conversation data
   - Provides fast relational queries
   - Maintains conversation metadata and timestamps

2. **Vector Database** (`vector_database.db`)
   - Stores conversation embeddings for semantic search
   - Enables similarity-based retrieval
   - Supports AI-powered analysis and recommendations

### Data Flow
```
Conversation Session → SQLite (structured storage) → Vector DB (embeddings)
                                    ↓
                              AI Analysis ← Vector DB (semantic retrieval)
```

### Synchronization
- Conversations are automatically added to both databases
- Vector database is populated immediately after SQLite storage
- Both databases maintain user_id-based partitioning for consistency

## Database Management

### Setup Database
```bash
python setup_database.py
```
This script:
- Creates the `conversation_history` table if it doesn't exist
- Migrates data from old `conv_hist` table if present
- Creates indexes for better performance

### View Conversations
```bash
# List all conversations
python view_conversations.py list

# View specific conversation
python view_conversations.py detail <conversation_id>

# View user's conversations
python view_conversations.py user <user_id>
```

### Database Statistics
The database manager provides statistics including:
- Total number of conversations
- Number of unique users
- Database size in MB

## Code Usage

### Using DatabaseManager
```python
from services.database import db_manager

# Save a conversation
conversation_id = db_manager.save_conversation(user_id, date, transcript)

# Get user's conversations
conversations = db_manager.get_conversations_by_user(user_id)

# Get specific conversation
conversation = db_manager.get_conversation_by_id(conversation_id)

# Get database stats
stats = db_manager.get_database_stats()
```

### Direct SQLite Access
```python
import sqlite3

conn = sqlite3.connect("conversation_history.db")
cursor = conn.cursor()

# Example query
cursor.execute("SELECT * FROM conversation_history WHERE user_id = ?", (user_id,))
conversations = cursor.fetchall()

conn.close()
```