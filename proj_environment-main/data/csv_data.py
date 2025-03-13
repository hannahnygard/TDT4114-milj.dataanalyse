import requests
import os
import csv
from dotenv import load_dotenv
import pandas as pd
import json
from io import StringIO

#laster opp variabler fra .env-fil
dotenv_path = "api_nokkel.env"
load_dotenv(dotenv_path=dotenv_path) 

#henter ut ut variabler fra .env-fil
api_key = os.getenv("API_KEY")

URL = "https://frost.met.no/observations/v0.jsonld"

by_oslo = "SN18700"

params = {
    "sources": by_oslo,
    "elements": "air_pressure_at_sea_level",  # lufttrykk
    "referencetime": "2023-01-01/2023-12-31",  # Setter tidsperiode
}

#response = requests.request("GET", URL, params=params, data={})
response = requests.get(URL, params=params, auth=(api_key, ""))

myjson = response.json()

#with open("data.json", "w") as f:
#    f.write(myjson)

df = pd.read_json(json.dumps(myjson))
df.to_csv()

with open("data.csv", "w") as f:
    f.write(json.dumps(myjson))
'''
respons = requests.get(URL, params=params, auth=(api_key, ""))


# Sjekk respons
if response.status_code == 200:
    data = response.json()
    print(data)  # Skriv ut eller bearbeid dataene

else:
    print("Feil:", response.status_code, response.text)

'''

