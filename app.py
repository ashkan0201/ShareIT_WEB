
# Required library
import os
import sqlite3
import werkzeug.utils
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime
from glob2 import glob

app = Flask(__name__, template_folder = "template")

# Empty the files that are in "files".
address = glob("files/*")
for file_path in address:
    os.remove(file_path)

# sql preparation
def sql_code(path):
    con = sqlite3.connect(path)
    cur = con.cursor()
    return con , cur

# Emptying things that are in the database
con,cur = sql_code("database/data_of_files.db")
cur.execute("DELETE FROM data")
con.commit()

# A function that calculates the volume
def format_size(size):
    units = ["B", "KB", "MB", "GB"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    size = round(size, 2)
    formatted_size = f"{size} {units[index]}"
    return formatted_size