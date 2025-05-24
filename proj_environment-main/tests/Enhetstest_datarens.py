import unittest
import pandas as pd
import sys, os
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_rens import DataRens

class Test_DataRens(unittest.TestCase):

    def setUp(self):      
        """
        Oppsettmetode som kjøres før hver test.

        Det opprettes en enkel DataFrame med to rader og lagres som JSON i en testfil 
        "testdata.json" i samme mappe som testfilen. Dette gjør at hver test starter med definert og kontrollert testdata.

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Formål:
        Oppretter en testklar versjon av "DataRens" klassen.
        ppretter en JSON-testfil med eksempeldata, slik at testene
        kan verifisere funksjonaliteten til klassens metoder.
        """

        # Oppretter en testfil med kjent datastruktur slik at vi kan kontrollere at funksjonen håndterer JSON-inndata riktig
        self.rens = DataRens()
        self.test_fil = os.path.join(os.path.dirname(__file__), 'testdata.json')

        df = pd.DataFrame([
            {"referencetime": "2024-01-01", "value": 10, "data": {"source": "test"}},
            {"referencetime": "2024-01-02", "value": 20, "data": {"source": "test2"}}
        ])
        df.to_json(self.test_fil, orient="records")



    def test_opprettelse_database(self):  
        """
        Tester funksjonen "database_opprettelse" i "DataRens".

        Fremgangsmåte:
        - Kaller "database_opprettelse" med testfilen som input.
        - Sjekker at databasen "frost_Database.db" blir opprettet i "../data/" mappen relativt til testfilen.

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.
    
        Formål:
        Sikre at funksjonen faktisk oppretter en databasefil på forventet plassering, og at
        databasefilen eksisterer etter funksjonskallet "assertTrue(os.path.exists())".
        """

        # Sikrer at funksjonen faktisk oppretter databasen slik forventet når den kjøres med en gyldig JSON-fil
        self.rens.database_opprettelse(self.test_fil)
        database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'frost_Database.db'))
        self.assertTrue(os.path.exists(database_path))
        


    def test_return_dataframe(self):
        """
        Tester at funksjonen `database_opprettelse` returnerer en DataFrame.

        Fremgangsmåte:
        - Kaller "database_opprettelse" med testfilen.
        - Bruker "assertIsInstance" for å sjekke at returverdien er en "pd.DataFrame".

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Formål:
        Verifiserer at funksjonen ikke bare oppretter en database,
        men også returnerer et gyldig pandas DataFrame-objekt.
        """

        # Verifiserer at funksjonen returnerer en DataFrame etter at dataene er hentet og lagret i databasen
        df = self.rens.database_opprettelse(self.test_fil)
        self.assertIsInstance(df, pd.DataFrame)



    def test_database_tabell(self):   #tester om det blir opprettet en tabell i databasen
        """
        Tester om tabellen 'tabell' blir opprettet i SQLite-databasen.

        Fremgangsmåte:
        - Kaller "database_opprettelse" med testfilen som input.
        - Oppretter en tilkobling til SQLite-databasen.
        - Utfører en spørring mot SQLite systemtabell "sqlite_master" for å sjekke om tabellen "tabell" finnes.
        - Lukker databasetilkoblingen.
        - Bruker "assertIsNotNone" for å kontrollere at tabellen eksisterer, og at den ikke returnerer None 

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Formål:
        Verifisere at metoden "database_opprettelse" oppretter en tabell med navnet "tabell" i databasen.
        """

        # Kjører funksjonen som skal opprette databasen og tabellen, for å sikre at opprettelsen faktisk skjer
        self.rens.database_opprettelse(self.test_fil)

        # Lager sti til databasefilen slik at vi kan koble til den opprettede databasen
        database_sti = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'frost_Database.db'))
        kobling = sqlite3.connect(database_sti)
        cursor = kobling.cursor()

        # Spørrer SQLite for å sjekke om tabellen med navn 'tabell' eksisterer i databasen
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tabell';")
        tabell = cursor.fetchone()   #retunerer none dersom tabellen ikke finnes

        kobling.close()

        # Tester at tabellen faktisk er opprettet, slik at videre databaseoperasjoner kan fungere
        self.assertIsNotNone(tabell)


    def test_database_til_dataframe(self):
        """
        Tester funksjonen "fra_database_til_dataframe" som henter data fra SQLite-databasen og konverterer det til en DataFrame.

        Fremgangsmåte:
        - Oppretter en testdatabase og tabellen "tabell" med kolonner som etterligner strukturen til det faktiske datasettet.
        - Setter inn en test rad som inneholder en JSON-struktur i kolonnen "data.observations".
        - Kaller funksjonen "fra_database_til_dataframe()" fra "DataRens".
        - Sjekker at resultatet har forventet kolonnenavn: ['referenceTime', 'values', 'unit'].
        - Sjekker at verdiene i første rad samsvarer med de som ble satt inn.

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Formål:
        Validere at data kan leses korrekt fra databasen og struktureres riktig i en DataFrame med ønskede kolonnenavn og verdier.
        """
        
        # Oppretter stien til testdatabasen slik at vi vet hvor vi skal lese/skrive data
        database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'frost_Database.db'))
        
        # Lager testinnhold for å etterligne et realistisk databaseinnslag med observasjoner i JSON-format
        test_data = '[{"value": 5.0, "unit": "mm"}]'

        # Bruker 'with' for å unngå at tilkoblingen til databasen blir hengende åpen og forårsaker feil i senere tester
        with sqlite3.connect(database_path) as kobling:
            cursor = kobling.cursor()
            
            # Oppretter tabellen for å sikre at funksjonen har riktig struktur å jobbe med
            cursor.execute('''
                CREATE TABLE tabell (
                    "data.referenceTime" TEXT,
                    "data.observations" TEXT,
                    "data.other_column_1" TEXT,
                    "data.other_column_2" TEXT
                )
            ''')

        # Setter inn data slik at funksjonen kan vise at den klarer å hente og tolke én rad riktig
        cursor.execute('''
            INSERT INTO tabell ("data.referenceTime", "data.observations", "data.other_column_1", "data.other_column_2")
            VALUES (?, ?, ?, ?)
        ''', ("2024-04-01T12:00:00Z", test_data, "Hei", "Hello"))
        kobling.commit()

        # Tester om funksjonen klarer å hente ut og transformere data korrekt fra databasen, noe som hjelper oss videre i koden
        df = self.rens.fra_database_til_dataframe()
        
        # Verifiserer at funksjonen faktisk returnerer forventet struktur, noe som er kritisk for videre bruk
        self.assertListEqual(list(df.columns), ['referenceTime', 'values', 'unit'])

        # Skjekker om key og value stemmer overens slik at vi vet at alt funker 
        self.assertEqual(df["referenceTime"].iloc[0], "2024-04-01T12:00:00Z")
        self.assertEqual(df["values"].iloc[0], 5.0)
        self.assertEqual(df["unit"].iloc[0], "mm") 



    def tearDown(self):
        """
        Oppryddingsfunksjon som kjøres etter hver testmetode.

        Handlinger:
        - Sletter JSON-testfilen "self.test_fil" hvis den eksisterer.
        - Finner og forsøker å slette SQLite-databasefilen "frost_Database.db" som er lagret i "../data/".
        - Håndterer eventuelt "PermissionError" hvis filen ikke kan slettes, noe som kan oppstå dersom den fortsatt er i bruk.

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Formål:
        Sikre at testmiljøet er rent etter hver testkjøring ved å slette midlertidige filer og databasen som ble brukt under testene.
        """

        # Fjerner testfilen for å unngå at neste test blir påvirket av gamle data
        if os.path.exists(self.test_fil):
            os.remove(self.test_fil)

        # Henter den absolutte stien til testdatabasen for å kunne rydde den bort etter hver test
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'frost_Database.db'))

        # Forsøker å slette databasen slik at hver test starter med en ren tilstand og ikke arver tidligere testdata
        if os.path.exists(db_path):
            try:
                os.remove(db_path)  
            except PermissionError:
                # Dette skjer for eksempel hvis databasen fortsatt er åpen i en annen prosess, noe som varsler brukeren
                print(f"Kan ikke fjerne filen {db_path}, den er i bruk.")

if __name__ == '__main__':
    unittest.main()






