#Handles all the DB work so it's not in main
# Check log for all inputs into the DB

#import importlib
import sqlite3 as sl
#con = sl.connect('Pokemon.db', check_same_thread=False)

#sql = ""
class DB_Handler:

    #This will connect to the database
    def __init__(self, DB):
        self.con = sl.connect(DB, check_same_thread=False)

    #This will run multiple commands
    def CallDB(self, command):
        with self.con:
            data = self.con.execute(command)
            return data

    # The following functions retrieve data from DB 
    # Retrieves all rows in a DB
    def RetrieveDB(self, table):
        data = self.CallDB(f"SELECT * FROM '{table}'")
        return (data)

    def RetrieveOrderedDB(self, table,column):
        data = self.CallDB(f"SELECT * FROM {table} ORDER BY {column}")
        return (data)
    
    def RetrieveCol(self, table, column):
        data = self.CallDB(f"SELECT {column} FROM {table}")
        return (data)

    def RetrieveCols(self, table, columns):
        query = "SELECT "
        for i in range (len(columns)):
            if i == len(columns)-1:
                query += f"{columns[i]} FROM {table}"
            else:
                query += f"{columns[i]}, "
            print (f"{i} {len(columns)}")
        data = self.CallDB(query)
        return data

    #maybe split into one for strings and one for ints
    def SearchDB(self, table, searchcol, searchrow):
        query = f"SELECT * FROM {table} WHERE {searchcol} = '{str(searchrow)}'"
        data = self.CallDB(query)
        return data
    
    #PRAGMA table_info(table_name);
    def getcollist(self, table):
        query = f"PRAGMA table_info('{table}');"
        data = self.CallDB(query)
        return data

    # retrieve a union of two table results
    def RetrieveUnionDB(self, table, searchcol, searchrow):
        print("not ready")

    #The following functions Change the DB
    #check comment on Search DB
    def UpdateDB(self, table, col, row, searchcol, searchrow):
        query = f"UPDATE {table} SET {col} = {row} WHERE {searchcol} =  {str(searchrow)}"
        data = self.CallDB(query)
        return data

    def InsertIntoDB(self, table, list):
        rows = str(list)[1:-1]
        self.CallDB(f"Insert INTO '{table}' VALUES ({rows})")
    
    #create a database if cols needs to be an array rows needs to be a 2d array
    def CreateDB(self, table, cols, rows):
        columns = str(cols)[1:-1]
        #columns = columns.replace("'", "")
        print(columns)
        self.CallDB(f"CREATE TABLE '{table}' ({columns})")
        if len(rows) > 0:
            for i in rows:
                print(i)
                self.InsertIntoDB(table, i)
    
    #drop table
    def DropDB(self, table):
        self.CallDB(f"DROP TABLE {table}")