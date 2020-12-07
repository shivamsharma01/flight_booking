import logging
import mysql.connector

class Database:
    # this function will be called when application is loaded. This db instance will be used across to access the db
    def __init__(self, host='localhost', user='root', password='Inm+jeto1', database='OOPD'):
        self._host = host
        self._user=user
        self._password=password
        self._database=database
        self._mydb=None
        self.createDBObject()
    
    def createDBObject(self):
        self._mydb = mysql.connector.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            database=self._database
        )
    
    def get_cursor(self):
        return self._mydb.cursor()
        
    def commit(self):
        logging.info('committing transaction')
        self._mydb.commit()

    def cursor_close(self):
        logging.info('closing cursor')
        self.get_cursor().close()

    def db_close(self):
        logging.info('closing connection')
        self._mydb.close()

