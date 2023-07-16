#import main
from DB_Handler import DB_Handler
import os
import display

# files = "test.csv"

DB = DB_Handler("Files.db")

#DB.CreateDB("Files", ["Name", "Path", "Table_name"], [])
#SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';
#data = DB.CallDB("Drop Table '/Users/robertludwick/Desktop/Python_Projects/DB_Handler/test.csv'")
#data = DB.CallDB("SELECT * FROM '/Users/robertludwick/Desktop/Python_Projects/DB_Handler/test.csv'")
data = DB.CallDB("PRAGMA table_info('/Users/robertludwick/Desktop/Python_Projects/DB_Handler/test.csv');")
# data = DB.getcollist("Files");
for i in data.fetchall():
    print(i)

#path = os.getcwd()

#print(main.database_compare(files, path))