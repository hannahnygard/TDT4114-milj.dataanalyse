import requests
import os 
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import json


# Leser inn .env-filen slik at API-nøkkelen kan holdes skjult fra koden
dotenv_path = "api_nokkel.env"
load_dotenv(dotenv_path=dotenv_path) 

# Henter API-nøkkelen slik at vi kan godkjenne forespørselen
api_key = os.getenv("API_KEY")

# Endepunkt for observasjonsdata fra Frost
URL = "https://frost.met.no/observations/v0.jsonld"
by_oslo = "SN18700"

# Parametere for å hente årlig gjennomsnitt mellom 1980 og 2020
parametere = {

    "sources": by_oslo,
    "referencetime": "1980-01-01/2020-12-31",
    "elements": "best_estimate_mean(air_temperature P1Y)"

}
 
# Sender forespørselen med autentisering for å få tilgang til data
response = requests.get(URL, params=parametere, auth=HTTPBasicAuth(api_key, ""))

# Sjekker om forespørselen gikk gjennom før vi lagrer noe
if response.status_code == 200:
    data = response.json()
    
else:
    print("feil:", response.status_code, response.text)


# Definerer hvor dataen skal lagres for senere bruk i analyse
filsti = os.path.join('data', 'frost_temp.json')

# Skriver dataen til en JSON-fil slik at vi slipper å hente data flere ganger
with open(filsti, 'w') as json_file:
    json.dump(data, json_file, indent=4)