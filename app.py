from nosql import get_data

import os
from flask import Flask, jsonify
from fuzzywuzzy import process
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/vehicle/match/<string:vehicle_name>', methods=['GET'])
def find_vehicle_match_short(vehicle_name):
    return find_vehicle_match(vehicle_name)

@app.route('/vehicle/match/<string:vehicle_name>/<int:year>', methods=['GET'])
def find_vehicle_match(vehicle_name, year=2017):
    print(f'{datetime.now()} // Calculating similarities ...')
    target_data = [v for v in get_data() if int(v['MANUFACTUREYEAR']) >= year and int(v['MODELYEAR']) >= year]
    selection = process.extractBests(query=vehicle_name, choices=[el["TRIM"] for el in target_data], limit=5)
    print(f"{datetime.now()} // Process finished, returning data ...")

    return_data = []
    for sel in selection:
        next_sel = next(vehicle for vehicle in get_data() if vehicle["TRIM"] == sel[0])
        if next_sel != None:
            next_sel['ACCURACY'] = sel[1]
        if next_sel != None and '_id' in next_sel:
            del next_sel['_id']
        return_data.append(next_sel)

    return jsonify(return_data)

from simulation.app import simulation_app
app.register_blueprint(simulation_app)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if(os.environ.get("ENV", "dev") == "dev"):
        app.run(port=port, debug=True)
    else:
        app.run(port=port)