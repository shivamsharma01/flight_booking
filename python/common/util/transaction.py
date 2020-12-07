from common.util.database import Database

class Transaction:
    def __init__(self):
        self._db = Database()
        self._cursor = self._db.get_cursor()
    
    def execute(self, query, tuple_data=None):
        if tuple_data is None:
            self._cursor.execute(query)
        else:
            self._cursor.execute(query, tuple_data)            
        return self._cursor.fetchone()

    def get_cursor(self):
        return self._cursor
    
    def close(self):
        self._db.commit()
        self._db.cursor_close()
        self._db.db_close()

