import unittest
import pandas as pd
import sys, os
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_rens import DataRens

class Test_DataRens(unittest.TestCase):

    def setUp(self):      #oppretter en jason fil med innhold for å kunne teste om de ulike funksjonene i klassen gjør det de skal
        self.rens = DataRens()
        self.test_fil = os.path.join(os.path.dirname(__file__), 'testdata.json')

        df = pd.DataFrame([
            {"referencetime": "2024-01-01", "value": 10, "data": {"source": "test"}},
            {"referencetime": "2024-01-02", "value": 20, "data": {"source": "test2"}}
        ])
        df.to_json(self.test_fil, orient="records")



    def test_opprettelse_database(self):  #tester om det faktisk opprettes en database
        self.rens.database_opprettelse(self.test_fil)
        database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'frost_Database.db'))
        self.assertTrue(os.path.exists(database_path))
        



    def test_return_dataframe(self): #tester om det lagres en dataframe i databasen
        df = self.rens.database_opprettelse(self.test_fil)
        self.assertIsInstance(df, pd.DataFrame)


    def test_database_tabell(self):   #tester om det blir opprettet en tabell i databasen
        self.rens.database_opprettelse(self.test_fil)
        database_sti = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'frost_Database.db'))
        kobling = sqlite3.connect(database_sti)
        cursor = kobling.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tabell';")
        tabell = cursor.fetchone()   #retunerer none dersom tabellen ikke finnes

        kobling.close()
        self.assertIsNotNone(tabell)


    def test_database_til_dataframe(self):
        #oppretter en test database og lager en kobling
        database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'frost_Database.db'))
        
        # Oppretter testdata
        test_data = '[{"value": 5.0, "unit": "mm"}]'


        # Bruker 'with' for å åpne og lukke forbindelsen automatisk
        with sqlite3.connect(database_path) as kobling:
            cursor = kobling.cursor()
            # Lager tabellen
            cursor.execute('''
                CREATE TABLE tabell (
                    "data.referenceTime" TEXT,
                    "data.observations" TEXT,
                    "data.other_column_1" TEXT,
                    "data.other_column_2" TEXT
                )
            ''')

        
        cursor.execute('''
            INSERT INTO tabell ("data.referenceTime", "data.observations", "data.other_column_1", "data.other_column_2")
            VALUES (?, ?, ?, ?)
        ''', ("2024-04-01T12:00:00Z", test_data, "Hei", "Hello"))
        kobling.commit()

        # Kjører funksjonen
        df = self.rens.fra_database_til_dataframe()
        
        #sjekker om key og value stemmer overens
        self.assertListEqual(list(df.columns), ['referenceTime', 'values', 'unit'])
        self.assertEqual(df["referenceTime"].iloc[0], "2024-04-01T12:00:00Z")
        self.assertEqual(df["values"].iloc[0], 5.0)
        self.assertEqual(df["unit"].iloc[0], "mm") 



    def tearDown(self):
        if os.path.exists(self.test_fil):   #fjerner dataen vi laget i testen og kjører etter hver test
            os.remove(self.test_fil)

        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'frost_Database.db'))

        #sletter databasefilen
        if os.path.exists(db_path):
            try:
                os.remove(db_path)  
            except PermissionError:
                print(f"Kan ikke fjerne filen {db_path}, den er i bruk.")

if __name__ == '__main__':
    unittest.main()






