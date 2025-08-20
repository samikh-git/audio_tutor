"""Utilities to expose database helpers to service modules.

Dynamically adjusts `sys.path` so that `server/database/database.py` can be
imported as `database` from sibling service modules, and re-exports the global
`db_manager`.
"""
import sys 
import os

# Add the database directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))

from database import db_manager

__all__ = ['db_manager']