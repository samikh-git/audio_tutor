#!/usr/bin/env python3
"""Conversation History Viewer utilities.

This script provides simple CLI commands to list recent conversations,
inspect a specific conversation, or view a user's conversation history.
"""

import sys
import os

# Add the database directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))

from database import db_manager

def view_conversations():
    """Print recent conversations and database statistics to stdout."""
    stats = db_manager.get_database_stats()
    
    print("=== Audio Tutor Database Statistics ===")
    print(f"Total conversations: {stats['total_conversations']}")
    print(f"Unique users: {stats['unique_users']}")
    print(f"Database size: {stats['database_size_mb']} MB")
    print()
    
    if stats['total_conversations'] == 0:
        print("No conversations found in database.")
        return
    
    # Get all conversations (limit to 20 for display)
    conn = db_manager._ensure_database_exists()
    import sqlite3
    conn = sqlite3.connect(db_manager.db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, user_id, session_date, created_at, 
               LENGTH(transcript) as transcript_length
        FROM conversation_history 
        ORDER BY created_at DESC
        LIMIT 20
    """)
    
    conversations = cursor.fetchall()
    conn.close()
    
    print("=== Recent Conversations ===")
    print(f"{'ID':<4} {'User ID':<15} {'Date':<12} {'Length':<8} {'Created'}")
    print("-" * 60)
    
    for conv in conversations:
        print(f"{conv[0]:<4} {conv[1]:<15} {conv[2]:<12} {conv[3]:<8} {conv[4]}")
    
    print()

def view_conversation_detail(conversation_id):
    """Print a specific conversation's metadata and full transcript.

    Args:
        conversation_id (int): Primary key of the conversation to display.
    """
    conversation = db_manager.get_conversation_by_id(conversation_id)
    
    if not conversation:
        print(f"Conversation with ID {conversation_id} not found.")
        return
    
    print(f"=== Conversation Details (ID: {conversation_id}) ===")
    print(f"User ID: {conversation['user_id']}")
    print(f"Session Date: {conversation['session_date']}")
    print(f"Created: {conversation['created_at']}")
    print(f"Transcript Length: {len(conversation['transcript'])} characters")
    print()
    print("=== Transcript ===")
    print(conversation['transcript'])

def view_user_conversations(user_id):
    """Print a summary list of a user's recent conversations.

    Args:
        user_id (str): Identifier used when saving conversations.
    """
    conversations = db_manager.get_conversations_by_user(user_id, limit=10)
    
    if not conversations:
        print(f"No conversations found for user: {user_id}")
        return
    
    print(f"=== Conversations for User: {user_id} ===")
    print(f"Total conversations: {len(conversations)}")
    print()
    
    for conv in conversations:
        print(f"ID: {conv['id']} | Date: {conv['session_date']} | Created: {conv['created_at']}")
        print(f"Transcript preview: {conv['transcript'][:100]}...")
        print("-" * 80)

def main():
    """Entry point for the CLI dispatcher.

    Usage:
        python view_conversations.py list
        python view_conversations.py detail <id>
        python view_conversations.py user <user_id>
    """
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python view_conversations.py list                    # List all conversations")
        print("  python view_conversations.py detail <id>            # View specific conversation")
        print("  python view_conversations.py user <user_id>         # View user's conversations")
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        view_conversations()
    elif command == "detail" and len(sys.argv) >= 3:
        try:
            conversation_id = int(sys.argv[2])
            view_conversation_detail(conversation_id)
        except ValueError:
            print("Error: Conversation ID must be a number")
    elif command == "user" and len(sys.argv) >= 3:
        user_id = sys.argv[2]
        view_user_conversations(user_id)
    else:
        print("Invalid command. Use 'list', 'detail <id>', or 'user <user_id>'")

if __name__ == "__main__":
    main() 