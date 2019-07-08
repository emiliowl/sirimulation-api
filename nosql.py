import os
import json
from pymongo import MongoClient

env = os.environ.get("ENV", "dev")
client = None

def load_from_mongo(client):
    vehicles_conn = client.vehicles
    return vehicles_conn.vehicles.find()

def load_from_failover():
    with open('vehicles.json', 'r') as file:
        data = file.read().replace('\n', '')
        registers = list(json.loads(data)["Vehicles"])
        return registers

def get_data():
    if env == "dev":
        client = MongoClient("localhost", 27017)
        return list(load_from_mongo(client))
    elif env == "failover":
        return list(load_from_failover())
    else:
        cert_path = os.path.dirname(os.path.realpath(__file__))
        client = MongoClient(
            "mongodb://admin:fDwT14qEMTvc2V9f@SG-Sirimulation-22916.servers.mongodirector.com:49076,SG-Sirimulation-22917.servers.mongodirector.com:49076,SG-Sirimulation-22918.servers.mongodirector.com:49076/admin?replicaSet=RS-Sirimulation-0&ssl=true",
            ssl=True,
            ssl_ca_certs=f'{cert_path}{os.path.sep}cert.pem')
        return list(load_from_mongo(client))