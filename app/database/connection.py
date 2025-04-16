import psycopg2
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
import streamlit as st
from app.config import load_config

class DatabaseConnection:
    """
    Manages database connections using a connection pool.
    Implements the Singleton pattern to ensure only one pool is created.
    """
    _instance = None
    _pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize_pool()
        return cls._instance
    
    def _initialize_pool(self):
        """Initialize the connection pool using configuration settings"""
        config = load_config()
        db_config = config["db"]
        
        try:
            self._pool = SimpleConnectionPool(
                1, 10,  # min_connections, max_connections
                dbname=db_config["name"],
                user=db_config["user"],
                password=db_config["password"],
                host=db_config["host"],
                port=db_config["port"]
            )
        except psycopg2.OperationalError as e:
            st.error(f"Error connecting to the database: {e}")
            st.stop()
    
    @contextmanager
    def get_connection(self):
        """Get a connection from the pool with context management"""
        if self._pool is None:
            self._initialize_pool()
            
        conn = self._pool.getconn()
        try:
            yield conn
        finally:
            self._pool.putconn(conn)
    
    @contextmanager
    def get_cursor(self):
        """Get a cursor with automatic transaction management"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()

# Global instance for easy access
db = DatabaseConnection() 