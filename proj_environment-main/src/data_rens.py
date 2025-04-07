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
        df = df[["year", "value", "unit"]].copy()

        # Telle duplikater før de fjernes
        antall_duplikater = df.duplicated(subset=["year"]).sum()
        print(f"Antall duplikater funnet: {antall_duplikater}")


    
        # Hvis duplikater finnes, fjern dem
        if antall_duplikater > 0:
            df = df.drop_duplicates()
            print("Duplikater er fjernet - antall rader: ", len(df))

        # Sjekk om det er noen manglende verdier
        manglende_år = df["value"].isna().sum()
        if manglende_år > 0:
            print(f"Antall år med manglende verdi: {manglende_år}")
            print("Rader uten verdi:")
            print(df[df["value"].isna()].to_string(index=False))  # Vist på en mer ryddig måte

            # Erstatter manglende verdier med gjennomsnttet fra alle årene
            gjennomsnitt = df["value"].mean().round(2)  
            df["value"] = df["value"].fillna(gjennomsnitt)  
            print("Manglende verdier er erstattet med gjennomsnittet: ", gjennomsnitt)

        else:
            print("Det er ingen datoer som mangler verdier!")


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
    






    
