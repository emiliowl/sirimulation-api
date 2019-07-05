import os
from flask import Flask
from fuzzywuzzy import process
from datetime import datetime

app = Flask(__name__)

@app.route('/simulation/<string:say_my_name>', methods=['GET', 'POST'])
def hello_world(say_my_name):
    ret = f'{datetime.now()} // Calculating similarities <br />'
    process.extract(say_my_name, database)
    selection = process.extractBests(query=say_my_name, choices=database, limit=5)
    for el in selection:
        ret = f"{ret}{datetime.now()} //{el[0]} x {say_my_name}: {el[1]}<br />"
    return ret

def initialize_database():
    text_file = open("nosql.txt", "r")
    lines = text_file.readlines()
    text_file.close()
    return lines

database = initialize_database()

if __name__ == '__main__' or __name__ == 'app':
    app.run()
