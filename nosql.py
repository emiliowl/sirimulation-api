import os
from pymongo import MongoClient

env = os.environ.get("ENV", "dev")
client = None

if env == "dev":
    client = MongoClient("localhost", 27017)
else:
    cert_path = os.path.dirname(os.path.realpath(__file__))
    client = MongoClient(
        "mongodb://admin:fDwT14qEMTvc2V9f@SG-Sirimulation-22916.servers.mongodirector.com:49076,SG-Sirimulation-22917.servers.mongodirector.com:49076,SG-Sirimulation-22918.servers.mongodirector.com:49076/admin?replicaSet=RS-Sirimulation-0&ssl=true",
        ssl=True,
        ssl_ca_certs=f'{cert_path}{os.path.sep}cert.pem')

vehicles_conn = client.vehicles
raw_data = vehicles_conn.vehicles.find()

def get_data():
    return list(raw_data)