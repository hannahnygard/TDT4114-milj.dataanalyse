import requests
import os 
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import json


#laster opp variabler fra .env-fil
dotenv_path = "api_nokkel.env"
load_dotenv(dotenv_path=dotenv_path) 

#henter ut ut variabler fra .env-fil
api_key = os.getenv("API_KEY")

URL = "https://frost.met.no/observations/v0.jsonld"
by_oslo = "SN18700"


# Parametere for forespørselen
parametere = {

    "sources": by_oslo,
    "referencetime": "1980-01-01/2020-12-31",
    "elements": "best_estimate_mean(air_temperature P1Y)"

}
 
# Send request
response = requests.get(URL, params=parametere, auth=HTTPBasicAuth(api_key, ""))

if response.status_code == 200:
    data = response.json()
    
else:
    print("feil:", response.status_code, response.text)


#Filsti for JSON-filen
filsti = os.path.join('data', 'frost_temp.json')
#Oppretter JSON-fil med dataen - lukker filen automatisk 
with open(filsti, 'w') as json_file:
    json.dump(data, json_file, indent=4)