import unittest
import pandas as pd
import sys, os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_rens import DataRens


class Test_DataRens(unittest.TestCase):
    def setUp(self):
        self.rens = DataRens()
        self.test_fil = os.path.join(os.path.dirname(__file__), 'testdata.json')

        # Korrekt struktur for JSON-fil (data skal være en ordbok med en liste under "data")
        test_json = {
            "data": [
                {
                    "sourceId": "123",
                    "referenceTime": "2020-01-01",
                    "observations": [
                        {
                            "elementId": "sum(precipitation_amount)",
                            "value": 100,
                            "unit": "mm",
                            "timeOffset": "PT0H",
                            "performanceCategory": "A"
                        },
                        {
                            "elementId": "sum(precipitation_amount)",
                            "value": 150,
                            "unit": "mm",
                            "timeOffset": "PT0H",
                            "performanceCategory": "A"
                        }
                    ]
                }   
            ]
        }

        # Oppretter filen med testdataen i setUp, slik at den kan brukes av testene
        with open(self.test_fil, "w", encoding="utf-8") as f:
            json.dump(test_json, f)




####################
#TESTING AV METODER SOM GÅR PÅ JSON-FILER

    def test_fra_json_til_dataframe(self):
        # Vi bruker filen som er laget i setUp
        testfil_sti = self.test_fil  

        #Kaller på funksjonen vi skal teste og leser fra testfilen
        df = self.rens.fra_json_til_dataframe(testfil_sti)

        #Sjekker at vi faktisk får tilbake en DataFrame
        self.assertIsInstance(df, pd.DataFrame)  

        #Sjekker at vi har riktig antall rader i tabellen
        self.assertEqual(len(df), 2)  
    
        #Sjekker at verdien på første rad er det vi satt inn
        self.assertEqual(df.iloc[0]["value"], 100)



    def test_nye_nedbor_verdier(self):
        # Lager en dataframe med year, value og unit
        df = pd.DataFrame([
            {"year": 2020, "value": 366, "unit": "mm"},  #Er skuddår
            {"year": 2021, "value": 365, "unit": "mm"}   #Er vanlig år
        ])
        resultat = self.rens.nye_nedbør_verdier(df)

        #Sjekker at antall dager er riktig for skuddår
        self.assertEqual(resultat.loc[0, "days"], 366)
        
        #Sjekker at verdien for skuddår er riktig 
        self.assertEqual(resultat.loc[0, "value"], 1.0)
        
        #Sjekker at verdien for et vanlig år er riktig 
        self.assertEqual(resultat.loc[1, "value"], 1.0)
        
        #Sjekker at kolonnen "total_values" finnes i resultatet
        self.assertIn("total_values", resultat.columns)


    def test_rens_dataframe(self):
        #Bruker testdata.json fra setUp-metoden
        testfil_sti = self.test_fil  # Filen som ble opprettet i setUp

        #kaller på metoden vi tester
        df = self.rens.fra_json_til_dataframe(testfil_sti)

        #Kaller på rens_DataFrame-metoden
        renset_df = self.rens.rens_DataFrame(df)

        #Sjekker om resultatet er en DataFrame
        self.assertIsInstance(renset_df, pd.DataFrame)

        #Sjekker at vi får riktig antallet rader etter rensingen
        self.assertEqual(len(renset_df), 2)  # Skal være 2 rader i dette eksempelet

        #sjekker kolonnenavnene 
        self.assertIn("value", renset_df.columns)

        #Sjekker at den henter riktig verdi
        self.assertEqual(renset_df.iloc[0]["value"], 100)       #Rad 1 fra testfilen




##########################################
#KJØRING AV TESTENE
if __name__ == "__main__":
    unittest.main()
