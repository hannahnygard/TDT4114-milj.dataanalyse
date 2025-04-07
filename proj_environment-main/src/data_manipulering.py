import json
import pandas as pd
import random

class DataManipulering:
    def __init__(self):
        pass


    def fjern_verdi_for_tilfeldig_aar(self, df):                #MANIPULERING
    # Velger et tilfeldig år mellom 1980 og 2020
        aar_for_fjerning = random.choice(range(1980, 2021))
    
        # Hent radene for dette året
        rader_for_aar = df[df["referenceTime"] == aar_for_fjerning]
    
        if not rader_for_aar.empty:
            # Velger en tilfeldig rad fra dette året og setter verdien til None
            tilfeldig_rad = rader_for_aar.sample(n=1)
            df.loc[tilfeldig_rad.index, "value"] = None
            print(f"Fjern verdi for år {aar_for_fjerning} (rad: {tilfeldig_rad.index[0]})")
        else:
            print(f"Fant ikke data for år {aar_for_fjerning}")
        return df
    

    def legg_til_duplikater_for_tilfeldig_aar(self, df):        #MANIPULERING
        # Velger et tilfeldig år mellom 1980 og 2020
        aar_for_duplikat = random.choice(range(1980, 2021))
    
        # Hent radene for dette året
        rader_for_aar = df[df["referenceTime"] == aar_for_duplikat]
    
        if not rader_for_aar.empty:
            # Dupliserer radene for dette året
            duplikater = rader_for_aar.sample(n=1, replace=True)  # Lager duplikater
            df = pd.concat([df, duplikater], ignore_index=True)
            print(f"Legger til duplikat for år {aar_for_duplikat}")
        else:
            print(f"Fant ikke data for år {aar_for_duplikat}")
    
        return df