import requests
from dotenv import load_dotenv
import os
import json

#laster opp variabler fra .env-fil
dotenv_path = "api_nokkel.env"
load_dotenv(dotenv_path=dotenv_path) 

#henter ut ut variabler fra .env-fil - kode hentet ut fra pensum-notebooken
api_key = os.getenv("API_KEY")

URL = "https://frost.met.no/observations/v0.jsonld"

by_oslo = "SN18700"

params = {
    "sources": by_oslo,
    "elements": "air_pressure_at_sea_level",  # lufttrykk
    "referencetime": "2023-01-01/2023-12-31",  # Setter tidsperiode
}

response = requests.get(URL, params=params, auth=(api_key, ""))

# Sjekker respons
if response.status_code == 200:
    data = response.json()

    #Lagrer dataen i en JSON-fil og legger til en filsti for hvor den skal bli lagret (i datamappen, ikke i rotmappen)
    filsti = os.path.join('data', 'frost_lufttrykk.json')
    with open(filsti, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Data lagret i frost_lufttrykk.json")

else:
    print("Feil:", response.status_code, response.text)

