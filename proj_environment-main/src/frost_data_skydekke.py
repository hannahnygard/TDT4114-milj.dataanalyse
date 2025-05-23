import requests
from dotenv import load_dotenv
import os
import json

# Leser inn .env-filen slik at API-nøkkelen kan holdes skjult fra koden
dotenv_path = "api_nokkel.env"
load_dotenv(dotenv_path=dotenv_path) 

# Henter API-nøkkelen slik at vi kan sende forespørsler til Frost
api_key = os.getenv("API_KEY")

# Endepunkt for observasjonsdata fra Frost
URL = "https://frost.met.no/observations/v0.jsonld"

by_oslo = "SN18700"

# Setter parametere for å hente årsmiddel av skydekke for Oslo, 1980–2020
params = {
    "sources": by_oslo,
    "elements": "mean(cloud_area_fraction P1Y)",  # Årsmiddel for skydekke: gjennomsnitt av tre daglige verdier 
    "referencetime": "1980-01-01/2020-12-31",  # Setter tidsperiode
}

# Henter data fra Frost ved å sende en GET-forespørsel med autentisering
response = requests.get(URL, params=params, auth=(api_key, ""))

# Sjekker om forespørselen gikk gjennom før vi lagrer noe
if response.status_code == 200:
    data = response.json()

    # Lagrer dataen i en JSON-fil og legger til en filsti for hvor den skal bli lagret (i datamappen, ikke i rotmappen) slik at vi kan bruke den videre i analyse
    filsti = os.path.join('data', 'frost_skydekke.json')
    with open(filsti, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Data lagret i frost_skydekke.json")

else:
    # Skriver ut feilmelding dersom noe gikk galt med forespørselen
    print("Feil:", response.status_code, response.text)

