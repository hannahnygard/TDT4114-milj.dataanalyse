import json
import pandas as pd


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
        #Leser dataene etter dato, før vi deretter beregner gjennomsnittet
        #df_nedbor_avg = df.groupby("referenceTime", as_index=False)["value"].mean()
        #df_nedbor_avg["unit"] = df.groupby("referenceTime")["unit"].first().reset_index(drop=True)

        #Telle duplikater før de fjernes
        def tell_duplikater():
            antall_duplikater = df_nedbor_avg.duplicated().sum()
            retur_av_duplikater = print(f"Antall duplikater funnet: {antall_duplikater}")

            #Dersom dataen har duplikater, blir de fjernet
            if antall_duplikater > 0:
                df_nedbor_avg.drop_duplicates(inplace=True)
            
            return retur_av_duplikater

        def finn_år_som_mangler_verdi():
            #Skjekker om det er noen år som mangler en verdi
            manglende_år = df_nedbor_avg["value"].isna().sum()
            if manglende_år > 0:
                print(f"Antall år med manglende verdi: {manglende_år}")
                print("År uten verdi:")
                print(df[df["value"].isna()])
            else:
                print("Det er ingen datoer som mangler verdier!")

        #Endrer "referencetime" til "year"
        df["year"] = pd.to_datetime(df["referenceTime"]).dt.year
      
        return df
    
    

    def nye_nedbør_verdier(df):
        #Sum per år
        df_nedbor_avg = df.groupby("year", as_index=False)["value"].sum()
        
        #Funksjon for å sjekke om et år er skuddår
        def er_skuddår(år):
            return (år % 4 == 0 and år % 100 != 0) or (år % 400 == 0)
        
        #Beregn gjennomsnitt per dag basert på om året er skuddår
        df_nedbor_avg["days"] = df_nedbor_avg["year"].apply(lambda x: 366 if er_skuddår(x) else 365)
        df_nedbor_avg["avg_per_day"] = (df_nedbor_avg["value"] / df_nedbor_avg["days"]).round(2)
        
        #Legger til unit etter avg_per_day
        df_nedbor_avg["unit"] = df_nedbor_avg["unit"].dropna().unique()[0] 

        return df_nedbor_avg
