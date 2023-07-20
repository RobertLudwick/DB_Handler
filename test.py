#import main
from src.DB_Handler import DB_Handler
import os
import src.display as display

file = "test.csv"

path = os.getcwd()

DB = DB_Handler("Files.db")