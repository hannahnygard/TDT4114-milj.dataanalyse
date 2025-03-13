import requests
import os
import csv
from dotenv import load_dotenv

#laster opp variabler fra .env-fil
dotenv_path = "api_nokkel.env"
load_dotenv(dotenv_path=dotenv_path) 

#henter ut ut variabler fra .env-fil
api_key = os.getenv("API_KEY")

URL = "https://frost.met.no/observations/v0.jsonld"

