import json
import pandas as pd
import random

class DataRens:
    def __init__(self):
        pass


    def fra_json_til_dataframe(self, filnavn):
        with open(filnavn, "r", encoding="utf-8") as f:
            data = json.load(f)
    
        #Henter observasjonene
        observationer = data.get("data", [])
    
        #Definerer tomme rader først
        rader = []
        for obs in observationer:
            source_id = obs.get('sourceId', None)
            reference_time = obs.get('referenceTime', None)


        #For hver observasjon kan vi lage en rad med informasjonen vi trenger
            for observation in obs.get('observations', []):
                rader.append({
                    'sourceId': source_id,
                    'referenceTime': reference_time,
                    'elementId': observation.get('elementId', None),
                    'value': observation.get('value', None),
                    'unit': observation.get('unit', None),
                    'timeOffset': observation.get('timeOffset', None),
                    'performanceCategory': observation.get('performanceCategory', None)
                })
    

        #Lag en Pandas DataFrame
        df = pd.DataFrame(rader)

        return df
    

    def rens_DataFrame(self, df):
        # Endre "referenceTime" til "year" først
        df["year"] = pd.to_datetime(df["referenceTime"]).dt.year

        # Beholder kun nødendige kolonner
        df = df[["year", "value", "unit"]]

        # Fjern verdi for et tilfeldig år
        df = self.fjern_verdi_for_tilfeldig_aar(df)  #TEST

        # Legg til duplikat for et tilfeldig år
        df = self.legg_til_duplikater_for_tilfeldig_aar(df)  #TEST

        # Telle duplikater før de fjernes
        antall_duplikater = df.duplicated(subset=["year"]).sum()
        print(f"Antall duplikater funnet: {antall_duplikater}")


    
        # Hvis duplikater finnes, fjern dem
        if antall_duplikater > 0:
            df.drop_duplicates(inplace=True)

        # Sjekk om det er noen manglende verdier
        manglende_år = df["value"].isna().sum()
        if manglende_år > 0:
            print(f"Antall år med manglende verdi: {manglende_år}")
            print("Uten verdi:")
            print(df[df["value"].isna()])
        else:
            print("Det er ingen datoer som mangler verdier!")


        return df
    



    def fjern_verdi_for_tilfeldig_aar(self, df):                #MANIPULERING
        # Velger et tilfeldig år mellom 1980 og 2020
        aar_for_fjerning = random.choice(range(1980, 2021))
        
        # Hent radene for dette året
        rader_for_aar = df[df["year"] == aar_for_fjerning]
        
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
        rader_for_aar = df[df["year"] == aar_for_duplikat]
        
        if not rader_for_aar.empty:
            # Dupliserer radene for dette året
            duplikater = rader_for_aar.sample(n=1, replace=True)  # Lager duplikater
            df = pd.concat([df, duplikater], ignore_index=True)
            print(f"Legger til duplikat for år {aar_for_duplikat}")
        else:
            print(f"Fant ikke data for år {aar_for_duplikat}")
        
        return df



    def nye_nedbør_verdier(self, df):
        # Lager en kopi av dataframen for å unngå feilmeldingen SettingsWithCopyWarning 
        df = df.copy()

        # Funksjon for å sjekke om det er skuddår
        def er_skuddår(år):
            return (år % 4 == 0 and år % 100 != 0) or (år % 400 == 0)

        # Legg til kolonnen 'days'
        df["days"] = df["year"].apply(lambda x: 366 if er_skuddår(x) else 365)

        # Legg til kolonnen 'avg_per_day'
        df["avg_per_day"] = df.apply(
                lambda row: round(row["value"] / row["days"], 2) if pd.notna(row["value"]) else None,
                axis=1
            )

        # Endrer til den rekkefølgen vi vil ha
        df = df[["year", "value", "avg_per_day", "unit", "days"]]

        return df
    






    
