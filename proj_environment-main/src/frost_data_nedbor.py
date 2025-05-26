import requests
from dotenv import load_dotenv
import os
import json


# Leser inn miljøvariabler for å unngå å hardkode API-nøkkelen i scriptet
dotenv_path = "api_nokkel.env"
load_dotenv(dotenv_path=dotenv_path) 

# Henter API-nøkkelen slik at vi kan godkjenne forespørselen
api_key = os.getenv("API_KEY")

# URL til Frost API for å hente observasjonsdata
URL = "https://frost.met.no/observations/v0.jsonld"
by_oslo = "SN18700"


# Setter hvilke data vi vil hente, fra hvor og hvilken tidsperiode
params = {
    "sources": "SN18700",
    "elements": "sum(precipitation_amount P1Y)",  # Nedbør per dag
    "referencetime": "1980-01-01/2020-12-31",  # Sett tidsperiode
}

# Sender en GET-forespørsel med tillatelse for å hente data fra Frost API
respons = response = requests.get(URL, params=params, auth=(api_key, ""))


# Sjekker om forespørselen var vellykket før vi fortsetter
if response.status_code == 200:
    data = response.json()
    #print(data)  # Skriv ut eller bearbeid dataene


    # Lagre dataen i en JSON-fil slik at den kan brukes senere
    filsti = os.path.join('data', 'frost_nedbor.json')
    with open(filsti, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Data lagret i frost_nedbor.json")

else:
    # Skriver ut feilmelding hvis noe gikk galt under forespørselen
    print("Feil:", response.status_code, response.text)

