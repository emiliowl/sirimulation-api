from nosql import get_data

import os, ssl
from flask import Flask, jsonify
from fuzzywuzzy import process
from datetime import datetime

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
database = get_data()

@app.route('/simulation/<string:say_my_name>', methods=['GET', 'POST'])
def hello_world(say_my_name):
    print(f'{datetime.now()} // Calculating similarities ...')
    selection = process.extractBests(query=say_my_name, choices=[el["TRIM"] for el in database], limit=5)
    print(f"{datetime.now()} // Process finished, returning data ...")

    return_data = []
    for sel in selection:
        next_sel = next(vehicle for vehicle in database if vehicle["TRIM"] == sel[0])
        if next_sel != None:
            next_sel['ACCURACY'] = sel[1]
        if next_sel != None and '_id' in next_sel:
            del next_sel['_id']
        return_data.append(next_sel)

    return jsonify(return_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if(os.environ.get("ENV", "dev") == "dev"):
        app.run(port=port, debug=True)
    else:
        app.run(port=port)
