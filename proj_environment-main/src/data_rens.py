import json
import pandas as pd
import sqlite3
import ast
import os
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display


class DataRens:
    def __init__(self):
        pass


    def database_opprettelse(self, filnavn ="frost_skydekke.json"):
        """
        Leser en JSON-fil og lagrer innholdet som en SQLite-database.

        Funksjonen leser en JSON-fil og konverterer innholdet til en pandas DataFrame. 
        Noe som sørger for at alle lister og ordbøker konverteres til strenger før dataen 
        lagres som en tabell i en SQLite-database. Databasen lagres i en undermappe kalt "data" 
        i prosjektstrukturen.

        Parametere:
        self (objekt): 
        Instansen av klassen denne metoden tilhører.
        filnavn (str): 
        Navn på JSON-filen som skal leses. Standardverdi er "frost_skydekke.json".

        Returnerer:
        En pandas DataFrame med dataen fra JSON-filen, klargjort og lagret i databasen. Det blir da
        opprettet en SQLite-databasefil kalt "frost_Database.db", og det kommer en 
        ny tabell med navn "tabell" i databasen. Funksjonen skriver ut bekreftelse til konsollen når operasjonen er vellykket.
        """

        #Noe kode inspirert av w3-schools, men ikke direkte kopiert

        # Leser JSON-filen slik at vi får tilgang til innholdet som et DataFrame-objekt
        df = pd.read_json(filnavn)

        # Gjør nested JSON-strukturer enklere å jobbe med ved å konvertere dem til en flat tabell
        df = pd.json_normalize(df.to_dict(orient="records"))

        # Unngår lagringsproblemer ved å gjøre lister og ordbøker om til tekstformat
        df = df.apply(lambda kolonne: kolonne.apply(lambda x: str(x) if isinstance(x, (dict, list)) else x))

        # Finner absolutt filsti til datamappen for å sikre korrekt lagring uansett hvor scriptet kjøres fra
        data_mappe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

        # Definerer hvor SQLite-databasen skal lagres for videre bruk
        database = os.path.join(data_mappe, 'frost_Database.db')

        # Kobler til databasen slik at vi kan lagre DataFrame som en SQL-tabell
        kobling = sqlite3.connect(database)

        # Erstatter eksisterende tabell slik at databasen alltid er oppdatert med nyeste data
        df.to_sql("tabell", kobling, if_exists= "replace", index=False)

        # Lukker tilkoblingen for å frigjøre ressurser og unngå feil
        kobling.close()

        print("Suksess! JSON er nå omgjort til en database")
        print()

        return df
    
    
    
    def fra_database_til_dataframe(self):
        """
        Leser data fra SQLite-databasen og returnerer en bearbeidet DataFrame.

        Funksjonen kobler seg til en eksisterende SQLite-database kalt "frost_Database.db",
        henter ut spesifikke kolonner fra tabellen "tabell", evaluerer nested struktur i
        kolonnen "data.observations", og trekker ut verdier og enheter fra observasjonene.
        Resultatet returneres som en ny, forenklet DataFrame.

        Parametere:
        self (objekt): 
        Instansen av klassen denne metoden tilhører.

        Returnerer:
        En DataFrame med kolonnene "referenceTime", "values" og "unit". Dersom noe går galt ved henting 
        eller behandling av data, skrives det ut en feilmelding til konsollen. Etter en utført operasjon
        lukkes databasen uasett om det oppstår feil eller ikke.
        """
        try:
            # Bruker absolutt sti slik at databasen alltid havner riktig uansett hvor scriptet kjøres fra
            data_mappe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
            
            # Setter opp filsti til SQLite-databasen så vi vet nøyaktig hvor den skal lagres
            database = os.path.join(data_mappe, 'frost_Database.db')

            # Knytter tilkobling til databasen for å hente ut informasjon
            kobling = sqlite3.connect(database)

            # Henter ut alle relevante kolonner, også nested data som "data.referenceTime" og "data.observations"
            query = """
            SELECT "data.referenceTime", "data.observations", "data.other_column_1", "data.other_column_2"
            FROM tabell
            """
            df = pd.read_sql_query(query, kobling)

            # Gjør tekstrepresentasjon av liste/ordbok om til ekte Python-objekter for videre behandling
            df["data.observations"] = df["data.observations"].apply(ast.literal_eval)

            # Henter ut første verdi hvis det finnes en liste med observasjoner
            df["values"] = df["data.observations"].apply(lambda x: x[0]["value"] if isinstance(x, list) and len(x) > 0 else None)

            # Henter ut enhet fra samme struktur som over, dersom tilgjengelig
            df["unit"] = df["data.observations"].apply(lambda x: x[0]["unit"] if isinstance(x, list) and len(x) > 0 else None)

            # Filtrerer til kun de mest relevante kolonnene for videre analyse
            df = df[["data.referenceTime", "values", "unit"]]

            # Forenkler kolonnenavn for enklere videre bruk
            df = df.rename(columns={"data.referenceTime": "referenceTime"})
           
        except Exception as feil:
            # Printer feilen dersom noe går galt med spørring eller konvertering
            print(f"Noe gikk galt: {feil}")

        finally:
            # Sørger for at tilkoblingen alltid lukkes, uansett om det oppstår feil eller ikke
            kobling.close()

        return df
    


    def fra_json_til_dataframe(self, filnavn):
        """
        Leser en JSON-fil og konverterer observasjonene til en strukturert DataFrame.

        Funksjonen åpner en spesifisert JSON-fil og henter ut observasjoner fra "data"-feltet.
        Hver observasjon kan inneholde flere måleverdier, og funksjonen bygger en rad per måling
        med tilhørende metadata. Til slutt returneres en DataFrame med alle relevante kolonner.

        Parametere:
        self (objekt): 
        Instansen av klassen denne metoden tilhører.
        filnavn (str): 
        Filbane til JSON-filen som skal leses.

        Returnerer:
        En DataFrame der hver rad representerer én måling, med kolonner som "sourceId", 
        "referenceTime", "elementId", "value", "unit","timeOffset" og "performanceCategory".
        """

        # Leser inn JSON-data for å kunne hente ut strukturert informasjon
        with open(filnavn, "r", encoding="utf-8") as f:
            data = json.load(f)
    
        # Henter ut selve observasjonene fra "data"-nøkkelen som inneholder målingene vi er interessert i
        observationer = data.get("data", [])
    
        # Forbereder en tom liste for å samle uttrukket informasjon fra hver observasjon
        rader = []
        for obs in observationer:
            # Henter felles metadata en gang per gruppe med observasjoner
            source_id = obs.get('sourceId', None)
            reference_time = obs.get('referenceTime', None)

        # Bygger en rad per faktisk måling under hver gruppe, slik at det kan struktureres som en tabell
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

        # Gjør den sammensatte listen av rader om til en strukturert DataFrame som kan analyseres videre
        df = pd.DataFrame(rader)

        return df
    


    def nye_nedbør_verdier(self, df):
        """
        Beregner gjennomsnittlig nedbør per dag for hvert år og oppdaterer DataFrame.

        Funksjonen legger til en kolonne med antall dager per år, tar hensyn til skuddår,
        og beregner gjennomsnittlig verdi per dag. Den totalnedbøren som tidligere lå i
        "value" kolonnen flyttes til "total_values", mens "value" nå representerer 
        gjennomsnittet per dag. Rekkefølgen på kolonnene tilpasses til ønsket struktur.

        Parametere:
        self (objekt): 
        Instansen av klassen denne metoden tilhører.
        df (pandas.DataFrame): 
        En DataFrame som må inneholde kolonnene "year", "value" og "unit".

        Returnerer:
        En oppdatert DataFrame med kolonnene "year", "total_values", "value" som å er gjennomsnitt per dag, "unit" og "days".
        Der det ikke er noen permanente endringer i original-DataFrame, da funksjonen opererer på en kopi.
        """

        # Lager en kopi av dataframen for å unngå feilmeldingen SettingsWithCopyWarning 
        df = df.copy()
        
        # Hjelpefunksjon for å avgjøre om året er et skuddår, for korrekt antall dager
        def er_skuddår(år):
            return (år % 4 == 0 and år % 100 != 0) or (år % 400 == 0)
        
        # Legger til en kolonne med antall dager i året, for å kunne beregne daglig snitt
        df["days"] = df["year"].apply(lambda x: 366 if er_skuddår(x) else 365)
        
        # Regner ut gjennomsnittlig nedbør per dag for hvert år, for mer meningsfull sammenligning
        df["avg_per_day"] = df.apply(
                lambda row: round(row["value"] / row["days"], 2) if pd.notna(row["value"]) else None,
                axis=1)
        
        # Gir mer presise navn på kolonner: skiller totalverdi og daglig gjennomsnitt
        df.rename(columns = {"value" : "total_values", "avg_per_day" : "value"}, inplace = True)
        
        # Reorganiserer kolonner for å gjøre datasettet lettere å lese og bruke
        df = df[["year", "total_values", "value", "unit", "days"]]
        return df



    def rens_DataFrame(self, df):
        """
        Renser og standardiserer DataFrame med nedbørsdata.

        Funksjonen standardiserer kolonnenavn, konverterer dato til år, fjerner duplikater,
        og håndterer manglende verdier. Den skriver også ut informasjon underveis for å vise
        hvor mange duplikater og manglende verdier som finnes, og hvilke rader som blir påvirket.

        Parametere:
        self (objekt): 
        Instansen av klassen denne metoden tilhører.
        df (pandas.DataFrame): 
        DataFrame med minst kolonnene "data.referenceTime" eller "referenceTime", "values" eller "value", og "unit".

        Returnerer:
        En renset og standardisert DataFrame med kolonnene "year", "value" og "unit". 
        Der duplikater og manglende verdier er håndtert, og antallet av hver type er skrevet ut til konsollen. 
        Rader med manglende verdier vises før de blir erstattet. Deretter erstattes de manglende 
        verdiene i kolonnen "value" med gjennomsnittet av kolonnen.
        """

        # Endrer data.referenceTime til referenceTime slik at det gir mer forståelse 
        if "data.referenceTime" in df.columns:
            df = df.rename(columns={"data.referenceTime": "referenceTime"})
        
        if "values" in df.columns:
            df = df.rename(columns={"values": "value"})

        # Endrer "referenceTime" til "year" for å kunne gruppere og analysere per år
        df["year"] = pd.to_datetime(df["referenceTime"]).dt.year

        # Fjerner unødvendige kolonner for å fokusere på relevante data
        df = df[["year", "value", "unit"]].copy()

        # Sjekker antall duplikater for å rydde opp i datasettet før videre bruk
        antall_duplikater = df.duplicated(subset=["year"]).sum()
        print(f"Antall duplikater funnet: {antall_duplikater}")

        # Fjerner duplikater for å sikre at hvert år kun har en observasjon
        if antall_duplikater > 0:
            df = df.drop_duplicates()
            print("Duplikater er fjernet - antall rader: ", len(df))

        # Undersøker om noen år mangler verdier som må håndteres
        manglende_år = df["value"].isna().sum()
        if manglende_år > 0:
            print(f"Antall år med manglende verdi: {manglende_år}")
            df_uten_fylling = df.copy()  
            print("Rader uten verdi:")
            print(df[df["value"].isna()].to_string(index=False))  # Gir bedre oversikt i utskrift

            # Fyller inn manglende verdier med gjennomsnittet for å bevare datastrukturen
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



    






    
