"""
Database Helper Module
Handles all database connections and operations for PostgreSQL
"""
import os
import psycopg2

from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

class DatabaseHelper:
    def __init__(self):
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            database_url = os.environ.get('DATABASE_URL')
            if database_url:
                self.connection = psycopg2.connect(database_url)
            else:
                self.connection = psycopg2.connect(
                    host=DB_CONFIG['host'],
                    user=DB_CONFIG['user'],
                    password=DB_CONFIG['password'],
                    database=DB_CONFIG['database']
                )
            return True
        except Error as e:

            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def is_connected(self):
        """Check if connection is open"""
        if self.connection and self.connection.closed == 0:
            return True
        return False

    def execute_query(self, query, params=None, fetch=False):
        """Execute a query and optionally fetch results"""
        try:
            # Ensure connection is active
            if not self.is_connected():
                if not self.connect():
                    print("Failed to establish database connection in execute_query")
                    return [] if fetch else False
            
            # Use RealDictCursor to mimic MySQL's dictionary=True
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                
                if fetch:
                    result = cursor.fetchall()
                    # Convert RealDict to standard dict for compatibility
                    return [dict(row) for row in result]
                else:
                    self.connection.commit()
                    # For INSERT statements, we might need a different way to get last ID in PG
                    # But often it's done via RETURNING clause in the query itself.
                    # As a fallback for simple EXECUTE:
                    try:
                        last_id = cursor.lastrowid
                    except:
                        last_id = True
                    return last_id
                    
        except Error as e:
            print(f"Query execution error: {e}")
            if self.connection:
                try:
                    self.connection.rollback()
                except Error:
                    pass
            return [] if fetch else False
        except Exception as e:
            print(f"Unexpected error in execute_query: {e}")
            return [] if fetch else False
    
    def execute_many(self, query, data_list):
        """Execute multiple queries with different parameters"""
        try:
            if not self.is_connected():
                self.connect()
            
            with self.connection.cursor() as cursor:
                cursor.executemany(query, data_list)
                self.connection.commit()
            return True
        except Error as e:
            print(f"Batch execution error: {e}")
            if self.connection:
                self.connection.rollback()
            return False

# Global database instance
db = DatabaseHelper()

