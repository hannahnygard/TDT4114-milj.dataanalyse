import json
import pandas as pd
import random

class DataManipulering:
    def __init__(self):
        pass


    def fjern_verdi_for_tilfeldig_aar(self, df):                

        #Sørger for at årskolonnen finnes - konverterer referenceTime til year
        if "year" not in df.columns:
            df["year"] = pd.to_datetime(df["referenceTime"]).dt.year

        # Velger et tilfeldig år mellom 1980 og 2020 som skal fjernes 
        aar_for_fjerning = random.choice(range(1980, 2021))
    
        # Henter radene som hører til dette året
        rader_for_aar = df[df["year"] == aar_for_fjerning]
    
        if not rader_for_aar.empty:
            # Velger en tilfeldig rad fra dette året og setter verdien til None
            tilfeldig_rad = rader_for_aar.sample(n=1)
            df.loc[tilfeldig_rad.index, "value"] = None
            print(f"Fjern verdi for år {aar_for_fjerning} (rad: {tilfeldig_rad.index[0]})")
        else:
            print(f"Fant ikke data for år {aar_for_fjerning}, kan ikke fjerne verdi.")
        return df
    

    def legg_til_duplikater_for_tilfeldig_aar(self, df):        
        # Konverterer referenceTime til datetime-format
        df["referenceTime"] = pd.to_datetime(df["referenceTime"], errors='coerce')

        # Henter år fra referenceTime
        df["year"] = df["referenceTime"].dt.year

        # Velger et tilfeldig år mellom 1980 og 2020
        aar_for_duplikat = random.choice(range(1980, 2021))
    
        # Hent radene for dette året
        rader_for_aar = df[df["year"] == aar_for_duplikat]
    
        if not rader_for_aar.empty:
            # Dupliserer radene for dette året
            duplikater = rader_for_aar.sample(n=1, replace=True)  # Lager duplikater
        
            # Fjerne de opprinnelige radene for dette året
            df = df[df["year"] != aar_for_duplikat]
        
            # Legg til de opprinnelige radene og duplikatene tilbake
            df = pd.concat([df, rader_for_aar, duplikater], ignore_index=True)
            df = df.sort_values(by="referenceTime")  # Sorterer DataFrame etter referenceTime

            print(f"Legger til duplikat for år {aar_for_duplikat}.")
            print(f'Totalt antall rader etter duplisering: {len(df)}.')
        else:
            print(f"Fant ikke data for år {aar_for_duplikat}, kan ikke legge til duplikat.")
    
        return df