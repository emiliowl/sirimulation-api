import os
import json
from pymongo import MongoClient

env = os.environ.get("ENV", "dev")
project_path = os.path.dirname(os.path.realpath(__file__))
host_ip_address = os.environ.get("HOST_IP_ADDRESS", "dev")
client = None

def load_from_mongo(client):
    vehicles_conn = client.vehicles
    return vehicles_conn.vehicles.find()

def load_from_failover():
    with open(f'{project_path}{os.path.sep}vehicles.json', 'r') as file:
        data = file.read().replace('\n', '')
        registers = list(json.loads(data)["Vehicles"])
        return registers

def get_data():
    if env == "dev":
        client = MongoClient(host_ip_address, 27017)
        return list(load_from_mongo(client))
    elif env == "failover":
        return list(load_from_failover())
    else:

        client = MongoClient(
            "mongodb://admin:fDwT14qEMTvc2V9f@SG-Sirimulation-22916.servers.mongodirector.com:49076,SG-Sirimulation-22917.servers.mongodirector.com:49076,SG-Sirimulation-22918.servers.mongodirector.com:49076/admin?replicaSet=RS-Sirimulation-0&ssl=true",
            ssl=True,
            ssl_ca_certs=f'{project_path}{os.path.sep}cert.pem')
        return list(load_from_mongo(client))