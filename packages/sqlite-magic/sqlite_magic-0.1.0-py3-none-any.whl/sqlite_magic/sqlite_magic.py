from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
import sqlite3
import pandas as pd

__all__ = ('SQLiteMagic', 'load_ipython_extension')

TABLE_INFO_COLUMNS = ['cid', 'name', 'type', 'notnull', 'default value', 'primary key']

@magics_class
class SQLiteMagic(Magics):
    
    def __init__(self, shell, connection=None):
        '''Initantiate with an empty SQLite connection'''
        super(SQLiteMagic, self).__init__(shell)
        self.connection = connection
        self.cursor = None if self.connection is None else self.connection.cursor()
        
    def __check_connection(self):
        if self.connection is None:
            raise RuntimeError("No database connection. Connect to a sqlite3 database using `%SQL_connect path` first.")
        return True
            

    @line_magic
    def SQL_connect(self, path):
        """ Connect to an SQLite3 database"""
        try:
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
        except:
            raise ValueError(f"Unable to connect to sqlite3 database at {path}")
    
    @line_magic
    def SQL_close_connection(self):
        '''Close the connection to the current database.'''
        self.connection.close()
        self.connection = None
        self.cursor = None
        
    @line_magic
    def SQL_tables(self, line):
        """ Returns a list of tables in the database."""
        assert self.__check_connection()
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return pd.DataFrame(self.cursor.fetchall(), columns=['Table'])
    
    @line_magic
    def SQL_PRAGMA(self, table):
        ''' Executes the PRAGMA command on table and returns the results in a dataframe.'''
        assert self.__check_connection()
        output = self.cursor.execute(f"PRAGMA table_info({table})").fetchall()
        return pd.DataFrame(output, columns=TABLE_INFO_COLUMNS)

    @line_magic
    def SQL_schema(self, table):
        ''' Executes the SQL schema of the table and returns the results in a dataframe.'''
        pragma = self.SQL_PRAGMA(table)
        return pragma[['name', 'type']]
    
    @cell_magic
    def SQL(self, line, cell):
        """ Execute the contents of a cell as a SQL query using pandas."""
        return pd.read_sql_query(cell, self.connection)



def load_ipython_extension(ipython):
    """
    Loads the SQLite magic with no connections.
    """
    magics = SQLiteMagic()
    ipython.register_magics(magics)
