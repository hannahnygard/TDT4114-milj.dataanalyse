import requests
import os 
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import json

#laster opp variabler fra .env-fil
load_dotenv() 

#henter ut ut variabler fra .env-fil
api_key = os.getenv("API_KEY")

URL = "https://frost.met.no/observations/v0.jsonld%22"

by_oslo = "SN18700"

# Parametere for forespørselen

parametere = {

    "sources": by_oslo,

    "referencetime": "1980-01-01/2020-02-01",

    "elements": "best_estimate_mean(air_temperature P1Y)"

}
 
# Send request
response = requests.get(URL, params=parametere, auth=HTTPBasicAuth(api_key, ""))

if response.status_code == 200:
    data = response.json()
    print(data)
    
else:
    print("feil:", response.status_code, response.text)


