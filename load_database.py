import json
from pymongo import MongoClient
import ssl

client = MongoClient("mongodb://admin:fDwT14qEMTvc2V9f@SG-Sirimulation-22916.servers.mongodirector.com:49076,SG-Sirimulation-22917.servers.mongodirector.com:49076,SG-Sirimulation-22918.servers.mongodirector.com:49076/admin?replicaSet=RS-Sirimulation-0&ssl=true",
                     ssl=True,
                     ssl_ca_certs='cert.pem')
vehicles_conn = client.vehicles

with open('vehicles.json', 'r') as file:
    data = file.read().replace('\n', '')
    registers = list(json.loads(data)["Vehicles"])
    vehicles_conn.vehicles.insert_many(registers)