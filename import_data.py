import json
import requests

id_eq_identity = True

with open('harvard_dataverse.json') as f:
    list_of_data = json.load(f)
    for item in list_of_data:
        requests.post("http://localhost:5000/data", json=item)
