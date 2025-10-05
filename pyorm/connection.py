from functools import cache
import sqlite3

class DbConnection:

    connection: sqlite3.Connection | None = None

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = self.connect()

    def connect(self):
        try:
            return sqlite3.connect(self.connection_string)
        except sqlite3.Error as e:
            raise ConnectionError(f"Failed to connect to database: {e}")
        finally:
            self.close()
    
    def execute(self, query: str, params: tuple | None = None):
        if not self.connection:
            self.connection = self.connect()
        cursor = self.connection.cursor()
        return cursor.execute(query, params or ())
    
    def commit(self):
        if not self.connection:
            self.connection = self.connect()
        self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
        self.connection = None


@cache
def get_db_connection(connection_string: str) -> DbConnection:
    return DbConnection(connection_string)
