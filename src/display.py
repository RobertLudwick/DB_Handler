import csv
import curses
from src.DB_Handler import DB_Handler
import os
from curses import wrapper

DB = DB_Handler("Files.db")

def open_file(filename):
    rows = []
    count = 0
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i in spamreader:
            if count == 0:
                cols = ','.join(i)
                if  i == "":
                    cols = ""
            else:
                rows.append(i)
            count+=1
        if count == 0:
            cols = ""
    return(cols,rows)

def add_file(file, path):
    contents, rows = open_file(file)
    cols = contents.split(",")
    DB.DropDB(f"{path}/{file}")
    DB.CreateDB(f"{path}/{file}", cols, rows)
    return (f"{path}/{file}")

def savefile(file, path):
    save = DB.RetrieveDB(f"{path}/{file}")
    cols = DB.getcollist(f"{path}/{file}")
    colcount = 0
    cols = cols.fetchall()
    for i in cols:
        colcount +=1
    f = open(file, "w")
    count = 1
    write = ""
    for i in cols:
        write += i[1]
        if colcount > count:
            write += ","
        else:
            write += "\n"
        count+=1
    count = 1
    for i in save.fetchall():
        for j in i:
            if j != None:
                write +=(j)
            if colcount > count:
                write += ","
            count+=1
        write += "\n"
        count = 1
    f.write(write[:-1])
        


def close_file(file, path):
    savefile(file, path)
    DB.DropDB(f"{path}/{file}")

def get_files():
    files = []
    search = os.listdir()
    for i in search:
        if ".csv" in i:
            files.append(str(i))
    return (files)

def command_execute(command):
    if command[0] == "new":
        f = open(command[1], "w")
        f.close()
    elif command[0] == "cd":
        os.chdir(command[1])
    # elif command[0] == "save":
    #     savefile(file, path)

def main(stdscr):
    # Clear screen
    path = os.getcwd()
    page = "select"
    stdscr.clear()
    bottom,right = stdscr.getmaxyx()
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
                #countrow += int(right/len())
            countcol+=1
            countrow=0
            for i in display.fetchall():
                for j in i:
                    stdscr.addstr(countcol, countrow, j)
                    # countrow += 13
                    countrow += int(right/len(i))
                    for k in range(right):
                        if k > countrow:
                            stdscr.addstr(countcol, k, (" "))
                countrow=0
                countcol+=1
            #stdscr.addstr(countcol, countrow, (table))
        if page == "query":
            query = query.replace("Table()", f"'{table}'")
            # try:
            result = DB.CallDB(query[1:])
            countcol = 0
            countrow = 0
            if '*' in query:
                for i in cols.fetchall():
                    stdscr.addstr(countcol, countrow, i[1])
            else:
                if 'select' in query.lower():
                    columns =query.split(" ")[1]
                    for i in columns.split(","):
                        stdscr.addstr(countcol, countrow, i)
                        countrow += int(right/len(columns.split(",")))
                else:
                    stdscr.addstr(countcol, countrow, f'{query[1:]}')
            countrow += 13
            #countrow += int(right/len())
            countcol+=1
            countrow=0
            for i in result.fetchall():
                for j in i:
                    stdscr.addstr(countcol, countrow, j)
                    #countrow += 13
                    countrow += int(right/len(i))
                    for k in range(right):
                        if k > countrow:
                            stdscr.addstr(countcol, k, (" "))
                countrow=0
                countcol+=1
            # except:
            #     stdscr.addstr(0, 0, f"{query[1:]}")
        for i in range(right):
            stdscr.addstr(int((bottom -bottom/4)), i, f'-')
        curses.echo()
        s = stdscr.getstr(int((bottom -bottom/4))+1,0, 320)
        command = str(s).replace("'", "")
        if command[1] == "/":
            com = command[2:].split(" ")
            stdscr.addstr(0, 0, com[0])
            if com[0] == "close":
                page = "display"
            if com[0] == "exit":
                running = False
            command_execute(com)
        else:
            if page == "display":
                query = str(s).replace("'", "")
                page = "query"
            if page == "select":
                file = str(s).replace("'", "")
                table = add_file(file[1:], path)
                page = "display"
        stdscr.clear()

#wrapper(main)