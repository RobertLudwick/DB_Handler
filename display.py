import csv
import curses
from DB_Handler import DB_Handler
import os
from curses import wrapper

DB = DB_Handler("Files.db")

def open_file(filename):
    rows = []
    count = 0
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for i in spamreader:
            if count == 0:
                cols = ','.join(i)
            else:
                rows.append(i)
            count+=1
    return(cols,rows)

def add_file(file, path):
    contents, rows = open_file(file)
    cols = contents.split(",")
    DB.CreateDB(f"{path}/{file}", cols, rows)
    DB.InsertIntoDB("Files", [file, path, f"{path}/{file}"])

def database_compare(file, path):
    csv_list = DB.SearchDB("Files", "Path", path)
    for i in csv_list.fetchall():
        if file == i[0]:
            return(i[2])
    add_file(file, path)
    database_compare(file, path)

def get_files():
    files = []
    search = os.listdir()
    for i in search:
        if ".csv" in i:
            files.append(str(i))
    return (files)

def main(stdscr):
    # Clear screen
    path = os.getcwd()
    page = "select"
    stdscr.clear()
    bottom = 24
    right = 80
    running = True
    while(running == True):        
        if page == "select":
            files = get_files()
            count = 0
            for i in files:
                stdscr.addstr(count, 0, i)
                count+=1
        if page == "display":
            display = DB.RetrieveDB(table)
            cols = DB.getcollist(table)
            countcol = 0
            countrow = 0
            for i in cols.fetchall():
                stdscr.addstr(countcol, countrow, i[1])
                countrow += 13
            countcol+=1
            countrow=0
            for i in display.fetchall():
                for j in i:
                    stdscr.addstr(countcol, countrow, j)
                    countrow += 13
                countrow=0
                countcol+=1
        if page == "query":
            query = query.replace("Table()", f"'{table}'")
            try:
                result = DB.CallDB(query[1:])
                countcol = 0
                countrow = 0
                if '*' in query:
                    for i in cols.fetchall():
                        stdscr.addstr(countcol, countrow, i[1])
                else:
                    stdscr.addstr(countcol, countrow, f'{query[1:]}')
                countrow += 13
                countcol+=1
                countrow=0
                for i in result.fetchall():
                    for j in i:
                        stdscr.addstr(countcol, countrow, j)
                        countrow += 13
                    countrow=0
                    countcol+=1
            except:
                stdscr.addstr(0, 0, f"{query[1:]}")
        for i in range(right):
            stdscr.addstr(bottom-5, i, f'-')
        curses.echo()
        s = stdscr.getstr(20,0, 320)
        if page == "display":
            query = str(s).replace("'", "")
            page = "query"
        if page == "select":
            file = str(s).replace("'", "")
            table = database_compare(file[1:], path)
            page = "display"
        stdscr.clear()

#wrapper(main)