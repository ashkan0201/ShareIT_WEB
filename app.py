
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

# Creating the main function to connect to the front end and send data to the web
@app.route('/')
def index():
    con,cur = sql_code("database/data_of_files.db")
    cur.execute("SELECT * FROM data")
    con.commit()
    files = cur.fetchall()
    return render_template('index.html', files = files)

# There are two parts to delete information and insert information in this section, which is related to sql
@app.route('/', methods = ['POST'])
def add_file():
    # Data deletion section
    try:
        delete_all_value = request.form.get('delete_all')
    except:
        delete_all_value = None
    if delete_all_value == "Delete All":
        con,cur = sql_code("database/data_of_files.db")
        cur.execute("DELETE FROM data")
        con.commit()
        address = glob("files/*")
        for file_path in address:
            os.remove(file_path)
        return redirect(url_for('index'))
    # Information collection section
    try:
        con,cur = sql_code("database/data_of_files.db")
        file = request.files['file']
        filename = werkzeug.utils.secure_filename(file.filename)
        if len(filename) >= 1:
            save_path = 'files/' + filename
        else:
            raise
        
        if os.path.isfile(save_path) == False:
            filename_parts = os.path.splitext(filename)
            file.seek(0, 2)
            file_size = file.tell()
            file.seek(0)
            formatted_size = format_size(file_size)
            data = (str(filename_parts[0]), str(filename_parts[1]), formatted_size, datetime.today().ctime())
            cur.execute("INSERT INTO data VALUES (?,?,?,?)",data)
            con.commit()
            con.close()
        else:
            raise
    except:
        pass
    else:
        file.save(save_path)
    return redirect(url_for('index'))

# To download files available on the web
@app.route('/download/<filename>', methods = ['GET'])
def download_file(filename):
    return send_from_directory('files', filename, as_attachment = True)

# Performance
if __name__ == '__main__':
    app.run(debug = True)