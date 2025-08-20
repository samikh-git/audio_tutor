import sys 
import os

# Add the database directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))

from database import db_manager

__all__ = ['db_manager']