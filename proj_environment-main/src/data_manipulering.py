import json
import pandas as pd
import random

class DataManipulering:
    def __init__(self):
        pass


    def fjern_verdi_for_tilfeldig_aar(self, df):                
        """
        Fjerner verdien i en tilfeldig rad for et tilfeldig valgt år mellom 1980 og 2020.

        Funksjonen sørger først for at en "year" kolonne eksisterer ved å hente ut år fra 
        "referenceTime" kolonnen om det er nødvendig. Deretter velges et tilfeldig år i 
        intervallet 1980-2020. Hvis datasettet inneholder rader for dette året, velges en 
        tilfeldig rad, og dens "value" kolonne settes til None.

        Parametere:
        self (objekt): 
        Instansen av klassen denne metoden tilhører.
        df (pandas.DataFrame): 
        Datasett som inneholder minst en "referenceTime" kolonne.
        Det bør også finnes en "value" kolonne for at funksjonen skal kunne sette verdien til None.

        Returnerer:
        En tuple med det oppdaterte DataFrame-objektet og ingen annen returverdi, og
        skriver ut hvilken rad og hvilket år som ble valgt for fjerning, eller beskjed 
        dersom ingen rader fantes for det valgte året.
        """

        # Sikrer at det finnes en "year" kolonne for enklere og mer lesbar tilgang til årstall senere i koden
        df["year"] = pd.to_datetime(df["referenceTime"]).dt.year

        # Velger et tilfeldig år mellom 1980 og 2020 for å simulere fjerning av en verdi i et tilfeldig valgt år
        aar_for_fjerning = random.choice(range(1980, 2021))
    
        # Henter radene som hører til dette året slik at det blir enklere fjerne en verdi senere
        rader_for_aar = df[df["year"] == aar_for_fjerning]
    
        if not rader_for_aar.empty:
            # Velger en tilfeldig rad innenfor det valgte året for å gjøre en spesifikk verdi ugyldig (None)
            tilfeldig_rad = rader_for_aar.sample(n=1)
            df.loc[tilfeldig_rad.index, "value"] = None
            print(f"Fjern verdi for år {aar_for_fjerning} (rad: {tilfeldig_rad.index[0]})")
        else:
            # Gir beskjed hvis det ikke finnes data for det valgte året, slik at man vet hvorfor ingen verdi ble fjernet
            print(f"Fant ikke data for år {aar_for_fjerning}, kan ikke fjerne verdi.")
        return df
    

    def legg_til_duplikater_for_tilfeldig_aar(self, df):  
        """
        Legger til én duplikat av en rad for et tilfeldig valgt år mellom 1980 og 2020.

        Funksjonen konverterer "referenceTime" kolonnen til datetime format, og henter ut året
        til en ny "year" kolonne. Deretter velges et tilfeldig år mellom 1980 og 2020.
        Hvis datasettet inneholder rader for dette året, dupliseres en tilfeldig rad.
        De originale radene for året og duplikatet legges så tilbake i datasettet, som
        til slutt sorteres etter "referenceTime".

        Parametere:
        self (objekt): 
        Instansen av klassen denne metoden tilhører.
        df (pandas.DataFrame): 
        Datasett som må inneholde en "referenceTime" kolonne i et datoformat som kan konverteres.

        Returnerer:
        En oppdatert DataFrame med en ekstra duplikat-rad, dersom det fantes data for det valgte året. 
        Ellers returneres datasettet uendret. Om en rad blir duplisert skrives det også ut hvilket år som ble valgt for duplisering, samt
        informerer om totalt antall rader etter at duplikatet er lagt til, og gir beskjed dersom det ikke finnes rader for det valgte året.
        """

        # Konverterer "referenceTime" til datetime-format for å sikre korrekt behandling av datoer videre i koden
        df["referenceTime"] = pd.to_datetime(df["referenceTime"], errors='coerce')
        
        # Trekker ut årstall fra "referenceTime" for å kunne gruppere og operere på data per år
        df["year"] = df["referenceTime"].dt.year

        # Velger et tilfeldig år mellom 1980 og 2020 for å simulere duplikering i et tilfeldig valgt år
        aar_for_duplikat = random.choice(range(1980, 2021))
    
        # Henter alle rader som tilhører det valgte året for å kunne lage duplikater av disse radene
        rader_for_aar = df[df["year"] == aar_for_duplikat]
    
        if not rader_for_aar.empty:
            # Lager en duplikat av en tilfeldig rad for å introdusere dupliserte data i datasettet
            duplikater = rader_for_aar.sample(n=1, replace=True)
        
            # Fjerner de originale radene for året midlertidig for å legge til både originaler og duplikater på nytt
            df = df[df["year"] != aar_for_duplikat]
        
            # Legger tilbake både de opprinnelige radene og duplikatene for å oppdatere datasettet med ekstra rader
            df = pd.concat([df, rader_for_aar, duplikater], ignore_index=True)

            # Sorterer datasettet etter "referenceTime" for å beholde kronologisk rekkefølge
            df = df.sort_values(by="referenceTime")

            print(f"Legger til duplikat for år {aar_for_duplikat}.")
            print(f'Totalt antall rader etter duplisering: {len(df)}.')
        else:
            # Informerer om at det ikke finnes data for valgt år, slik at vi vet hvorfor ingen duplikater ble lagt til
            print(f"Fant ikke data for år {aar_for_duplikat}, kan ikke legge til duplikat.")

        return df