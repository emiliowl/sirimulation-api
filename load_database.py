from pymongo import MongoClient
import os
import json

def load_to_mongo(vehicles_conn):
    print("Verifying if loading database is necessary...")
    load_size = len(list(vehicles_conn.vehicles.find()))
    if load_size == 0:
        print("Yah, lets load it !")
        with open('vehicles.json', 'r') as file:
            data = file.read().replace('\n', '')
            registers = list(json.loads(data)["Vehicles"])
            vehicles_conn.vehicles.insert_many(registers)
    else:
        print("It was already loaded, skipping...")
    print("Loading process completed! Enjoy!")


def load_to_failover_file():
    print("Verifying if loading database is necessary...")
    print("It was already loaded, skipping...")
    print("Loading process completed! Enjoy!")


env = os.environ.get("ENV", "dev")
client = None

if env == "dev":
    client = MongoClient("localhost", 27017)
    load_to_mongo(client.vehicles)
if env == "failover":
    load_to_failover_file()
else:
    cert_path = os.path.dirname(os.path.realpath(__file__))
    client = MongoClient(
        "mongodb://admin:fDwT14qEMTvc2V9f@SG-Sirimulation-22916.servers.mongodirector.com:49076,SG-Sirimulation-22917.servers.mongodirector.com:49076,SG-Sirimulation-22918.servers.mongodirector.com:49076/admin?replicaSet=RS-Sirimulation-0&ssl=true",
        ssl=True,
        ssl_ca_certs=f'{cert_path}{os.path.sep}cert.pem')
    load_to_mongo(client.vehicles)