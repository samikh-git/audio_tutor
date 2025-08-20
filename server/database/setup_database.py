#!/usr/bin/env python3
"""
Database setup script for Audio Tutor
Creates the required tables and cleans up database organization
"""

import sqlite3
import os
from datetime import datetime

def setup_database():
    """Create the conversation history table and clean up database"""
    
    # Connect to the database
    db_path = "./conversation_history.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Setting up database: {db_path}")
    
    # Create the conversation history table
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
    
    # Create an index for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_date 
        ON conversation_history(user_id, session_date)
    """)
    
    # Check if the old conv_hist table exists and migrate data if needed
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='conv_hist'
    """)
    
    if cursor.fetchone():
        print("Found old conv_hist table, migrating data...")
        
        # Get data from old table
        cursor.execute("SELECT * FROM conv_hist")
        old_data = cursor.fetchall()
        
        # Insert into new table
        for row in old_data:
            try:
                cursor.execute("""
                    INSERT INTO conversation_history (user_id, session_date, transcript)
                    VALUES (?, ?, ?)
                """, (row[0], row[1], row[2]))
            except Exception as e:
                print(f"Error migrating row: {e}")
        
        # Drop the old table
        cursor.execute("DROP TABLE conv_hist")
        print("Migration completed and old table dropped")
    
    # Commit changes
    conn.commit()
    
    # Show table structure
    print("\nDatabase tables:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        print(f"  - {table[0]}")
    
    # Show conversation_history structure
    print("\nConversation history table structure:")
    cursor.execute("PRAGMA table_info(conversation_history)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    conn.close()
    print("\nDatabase setup completed successfully!")

if __name__ == "__main__":
    setup_database() 