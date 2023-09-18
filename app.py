
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