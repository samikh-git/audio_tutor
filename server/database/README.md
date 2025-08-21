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

#### Optimization Tips
1. **Use appropriate k values** for similarity search (k=5-10 for analysis)
2. **Filter by namespace** to improve search performance
3. **Regular backups** of the vector database
4. **Monitor database size** as it grows with conversations

### Vector Database Troubleshooting

#### Common Issues
1. **Connection errors**: Check if Milvus is properly installed
2. **Empty results**: Verify documents exist for the user_id
3. **Performance issues**: Consider using different index types for larger datasets

#### Debugging
```python
# Test vector database functionality
from analyzer_tutor import vector_store, add_document

# Add test document
add_document("Test conversation content", "test_user")

# Test retrieval
results = vector_store.similarity_search("test", k=1, search_kwargs={"expr": 'namespace == "test_user"'})
print(f"Retrieved {len(results)} documents")
```

#### Dependencies
Required packages for vector database functionality:
```bash
pip install langchain-milvus
pip install pymilvus
pip install milvus-lite
```

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

## Best Practices

### SQLite Database
1. **Always use parameterized queries** to prevent SQL injection
2. **Use the DatabaseManager class** for consistent database operations
3. **Commit transactions** after write operations
4. **Close connections** when done
5. **Backup the database** regularly

### Vector Database
1. **Use appropriate search parameters** (k value, filters) for optimal performance
2. **Filter by namespace** to improve search accuracy and speed
3. **Monitor embedding quality** by testing retrieval results
4. **Backup both databases** together to maintain consistency
5. **Use meaningful queries** for semantic search (avoid single words)
6. **Test retrieval functionality** regularly to ensure proper operation

## Troubleshooting

### Multiple .db files
If you see multiple database files, check:
1. Database path in your code
2. Ensure you're connecting to the correct database file
3. Run `setup_database.py` to consolidate

### Database locked errors
- Close all connections before running maintenance
- Check for WAL mode files
- Restart the application if needed

## Maintenance

### Backup Database
```bash
cp conversation_history.db conversation_history_backup.db
```

### Clean up WAL files
```bash
sqlite3 conversation_history.db "PRAGMA wal_checkpoint(TRUNCATE);"
```

### Vacuum Database
```bash
sqlite3 conversation_history.db "VACUUM;"
``` 