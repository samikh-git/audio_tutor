#!/usr/bin/env python3
"""Database utilities for Audio Tutor.

Exposes a `DatabaseManager` class with helpers to create tables and perform
CRUD operations on the `conversation_history` SQLite database. A global
`db_manager` instance is created for convenience.
"""

import sqlite3
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
import os

class DatabaseManager:
    """Manage conversation history persistence in SQLite.

    If `db_path` is omitted, a database named `conversation_history.db` in the
    same directory as this module is used.
    """
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Use absolute path to the database directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(current_dir, "conversation_history.db")
        else:
            self.db_path = db_path
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Create the backing database and required tables if missing."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create conversation history table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_date DATE NOT NULL,
                transcript TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_date 
            ON conversation_history(user_id, session_date)
        """)
        
        conn.commit()
        conn.close()
    
    def save_conversation(self, user_id: str, session_date: date, transcript: str) -> int:
        """Insert a conversation session.

        Args:
            user_id (str): User identifier.
            session_date (date): Date of the session.
            transcript (str): Full transcript including prompts and replies.

        Returns:
            int: The auto-incremented conversation id.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversation_history (user_id, session_date, transcript)
            VALUES (?, ?, ?)
        """, (user_id, session_date, transcript))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return conversation_id
    
    def get_conversations_by_user(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Fetch recent conversations for a user.

        Args:
            user_id (str): User identifier.
            limit (int): Maximum number of rows to return.

        Returns:
            List[Dict]: List of conversation records.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, user_id, session_date, transcript, created_at
            FROM conversation_history 
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))
        
        conversations = []
        for row in cursor.fetchall():
            conversations.append({
                'id': row[0],
                'user_id': row[1],
                'session_date': row[2],
                'transcript': row[3],
                'created_at': row[4]
            })
        
        conn.close()
        return conversations
    
    def get_conversation_by_id(self, conversation_id: int) -> Optional[Dict]:
        """Fetch a conversation by its primary key.

        Args:
            conversation_id (int): Primary key.

        Returns:
            Optional[Dict]: Conversation row or None if not found.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, user_id, session_date, transcript, created_at
            FROM conversation_history 
            WHERE id = ?
        """, (conversation_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'user_id': row[1],
                'session_date': row[2],
                'transcript': row[3],
                'created_at': row[4]
            }
        return None
    
    def delete_conversation(self, conversation_id: int) -> bool:
        """Delete a conversation by its primary key.

        Args:
            conversation_id (int): Primary key.

        Returns:
            bool: True if a row was deleted.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM conversation_history WHERE id = ?", (conversation_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_database_stats(self) -> Dict:
        """Return basic database statistics and size information.

        Returns:
            Dict: Stats for total conversations, unique users, and DB size.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total conversations
        cursor.execute("SELECT COUNT(*) FROM conversation_history")
        total_conversations = cursor.fetchone()[0]
        
        # Unique users
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM conversation_history")
        unique_users = cursor.fetchone()[0]
        
        # Database size
        db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
        
        conn.close()
        
        return {
            'total_conversations': total_conversations,
            'unique_users': unique_users,
            'database_size_bytes': db_size,
            'database_size_mb': round(db_size / (1024 * 1024), 2)
        }

    def log_new_user(self, user_id, password, first_name, last_name ):
        return

    def user_id_already_exists(self, user_id):
        return

# Global database manager instance
db_manager = DatabaseManager() 