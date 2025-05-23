import json
import pandas as pd
import sqlite3
import ast
import os
import matplotlib.pyplot as plt


class DataRens:
    def __init__(self):
        pass

    def database_opprettelse(self, filnavn ="frost_skydekke.json"):
        #noe kode inspirert av w3-schools, men ikke direkte kopiert

        #Leser dataen fra json filen
        df = pd.read_json(filnavn)

        #Konverter dataen til en dict også videre til en todimensjonal tabell
        df = pd.json_normalize(df.to_dict(orient="records"))

        #Går gjennom kolonne for kolonne. Dersom x er en liste eller dict blir den konvertert til en streng, er den ikke det forblir x uendret
        df = df.apply(lambda kolonne: kolonne.apply(lambda x: str(x) if isinstance(x, (dict, list)) else x))

        #Viser til hvor databasen skal bli opprettet
        data_mappe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

        #Lager en filsti til hvor databsen skal opprettes
        database = os.path.join(data_mappe, 'frost_Database.db')

        #Bruker modulen sqlite3 for å koble oss opp til databasen vår
        kobling = sqlite3.connect(database)

        #Lagrer dataframen som en sql tabell
        df.to_sql("tabell", kobling, if_exists= "replace", index=False)

        kobling.close()

        print("Suksess! JSON er nå omgjort til en database")
        print()

        return df
    
    
    
    def fra_database_til_dataframe(self):
        try:
            #Viser til hvor databasen skal bli opprettet
            data_mappe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

            #Lager en filsti til hvor databsen skal opprettes
            database = os.path.join(data_mappe, 'frost_Database.db')

            kobling = sqlite3.connect(database)


            # Hent ut alle kolonner, inkludert 'data.referenceTime'
            query = """
            SELECT "data.referenceTime", "data.observations", "data.other_column_1", "data.other_column_2"
            FROM tabell
            """
            df = pd.read_sql_query(query, kobling)

            # Konvertere observasjoner
            df["data.observations"] = df["data.observations"].apply(ast.literal_eval)

            df["values"] = df["data.observations"].apply(lambda x: x[0]["value"] if isinstance(x, list) and len(x) > 0 else None)
            df["unit"] = df["data.observations"].apply(lambda x: x[0]["unit"] if isinstance(x, list) and len(x) > 0 else None)

            df = df[["data.referenceTime", "values", "unit"]]
            df = df.rename(columns={"data.referenceTime": "referenceTime"})
           
        except Exception as feil:
            print(f"Noe gikk galt: {feil}")

        finally:
            kobling.close()

        return df
    
    


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
                axis=1)
        
        df.rename(columns = {"value" : "total_values", "avg_per_day" : "value"}, inplace = True)
        
        #Endrer til den rekkefølgen vi vil ha
        df = df[["year", "total_values", "value", "unit", "days"]]
        return df



    def rens_DataFrame(self, df, vis_manglende=False):
        # Endrer data.referenceTime til referenceTime
        if "data.referenceTime" in df.columns:
            df = df.rename(columns={"data.referenceTime": "referenceTime"})
        
        # Values endres til value
        if "values" in df.columns:
            df = df.rename(columns={"values": "value"})


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
            df_uten_fylling = df.copy()  
            print("Rader uten verdi:")
            print(df[df["value"].isna()].to_string(index=False))  # Vist på en mer ryddig måte

            # Erstatter manglende verdier med gjennomsnttet fra alle årene
            gjennomsnitt = df["value"].mean().round(2)  
            df["value"] = df["value"].fillna(gjennomsnitt)  
            print("Manglende verdier er erstattet med gjennomsnittet: ", gjennomsnitt)

            if vis_manglende:
                self.plot_manglende_data(df_uten_fylling, df)

        else:
            print("Det er ingen datoer som mangler verdier!")


        return df
    
    def plot_manglende_data(self, df_med_hull, df_utfylt):
        plt.figure(figsize=(10, 6))
        plt.plot(df_med_hull["year"], df_med_hull["value"], 'o-', label="Med manglende verdier")
        plt.plot(df_utfylt["year"], df_utfylt["value"], 'o--', label="Etter utfylling")
        plt.xlabel("År")
        plt.ylabel("Verdi")
        plt.title("Effekt av manglende verdier på trend")
        plt.legend()
        plt.grid(True)
        plt.show()



    






    
