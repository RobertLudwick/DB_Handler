# DB_Handler (WIP Title)
An in terminal csv viewer and sqlite client. Using pythons Sqlite package and some functions I wrote to run common sql commands you can, easily implement databases into your projects, use the client I built to manage already existing Databases and view and and edit csv files with sql commands as if they were a database .

## The files

### DB_Handler.py
The start of this project and where it gets it's current name from. Referencing this file will grant you access to the pre written database interface functions allowing you to create tables, modify them, and search them all while calling simple functions with a few inputs.

### Example
```python
def RetrieveOrderedDB(self, table,column):
    data = self.CallDB(f"SELECT * FROM {table} ORDER BY {column}")
    return (data)
```

### display.py
This is all the code necessary for the in terminal UI, except for what is handled by DB_Handler.py. csv files need to be in the projec folder to be detected for now.

### main.py
calls the main function in display.py 

### Test.py
File for me to test the functions I write in main.py without the UI.