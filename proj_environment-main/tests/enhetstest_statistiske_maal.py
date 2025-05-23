import pandas as pd
import os, sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from statistiske_maal import Statistiske_maal


class Test_Statistiske_maal(unittest.TestCase):

    def setUp(self):             #funksjonen kjører før hver test og setter opp testdata
        data = {
            "year": list(range(1980, 2021)),
            "value": list(range(1, 42))  # 1980–2020 = 41 år
        }
        
        self.df = pd.DataFrame(data)
        self.sm = Statistiske_maal()
    
    def test_gjennomsnitt(self):     
        result = self.sm.gjennomsnitt(self.df)

        # sammenligner resultatene fra funksjonen med de forventede verdiene
        #verdiene for 1980-1989 er 1-10, deler dette på 10 og sammenligner med resultatene fra gjennomsnittsfunksjonen
        self.assertEqual(result["1980-1989"], round(sum(range(1, 11)) / 10, 2))  
        self.assertEqual(result["1990-1999"], round(sum(range(11, 21)) / 10, 2))
        self.assertEqual(result["2000-2009"], round(sum(range(21, 31)) / 10, 2))
        self.assertEqual(result["2010-2020"], round(sum(range(31, 42)) / 11, 2))
        self.assertEqual(result["Totalt"], round(sum(range(1, 42)) / 41, 2))


    def test_ugyldige_gjennomsnitt(self):
        # tester om funksjonen hånterer ugyldige verdier på riktig måte
        df = pd.DataFrame({
        "year": [1980, 1981, 1982],
        "value": ["en", "to", "tre"] 
    })
        with self.assertRaises((TypeError, ValueError)):
            self.sm.gjennomsnitt(df)


    def test_median(self):
        
        result = self.sm.median(self.df)
        
        #sammenligner medianen fra funksjonen med den forventede medianen
        self.assertEqual(round(result["1980-1989"], 2), 5.5)  # medianen for 1-10 er 5.5
        self.assertEqual(round(result["1990-1999"], 2), 15.5)
        self.assertEqual(round(result["2000-2009"], 2), 25.5)
        self.assertEqual(round(result["2010-2020"], 2), 36.0)
        self.assertEqual(round(result["Totalt"], 2), 21.0)

    def test_ugyldig_median(self):
        # tester om funksjonen er i stand til å håndtere ugyldige år
        df = pd.DataFrame({
        "year": ["a","b", "c"],
        "value": [30, 1, 24]
    })

        with self.assertRaises((TypeError, ValueError)):
            self.sm.median(df)

    def test_standardavvik(self):
        result = self.sm.standardavvik(self.df)

        #bruker pandas std() for å beregne standardavviken og sammenligne dette med det funksjonene regner ut
        self.assertEqual(round(result["1980-1989"], 2), round(self.df[(self.df["year"] >= 1980) & (self.df["year"] <= 1989)]["value"].std(), 2))
        self.assertEqual(round(result["1990-1999"], 2), round(self.df[(self.df["year"] >= 1990) & (self.df["year"] <= 1999)]["value"].std(), 2))
        self.assertEqual(round(result["2000-2009"], 2), round(self.df[(self.df["year"] >= 2000) & (self.df["year"] <= 2009)]["value"].std(), 2))
        self.assertEqual(round(result["2010-2020"], 2), round(self.df[(self.df["year"] >= 2010) & (self.df["year"] <= 2020)]["value"].std(), 2))
        self.assertEqual(round(result["Totalt"], 2), round(self.df[(self.df["year"] >= 1980) & (self.df["year"] <= 2020)]["value"].std(), 2))

    def ugyldig_standardavvik(self):
        # tester om funksjonen er i stand til å håndtere ugyldige verdier 
        df = pd.DataFrame({
        "year": [2000, 2001, 2002],
        "value": ["lav", "middels", "høy"]
    })

        with self.assertRaises((TypeError, ValueError)):
            self.sm.standardavvik(df)

    def test_tom_dataframe(self): 
        # sjekker hvordan håndteringen av et tomt datasett blir
        
        tom_df = pd.DataFrame(columns=["year", "value"])
        resultat_avg = self.sm.gjennomsnitt(tom_df)
        resultat_median = self.sm.median(tom_df)
        resultat_std = self.sm.standardavvik(tom_df)

        for key in ["1980-1989", "1990-1999", "2000-2009", "2010-2020", "Totalt"]:
            # sjekker om verdien er NaN før vi prøver å runde
            self.assertTrue(pd.isna(resultat_avg[key]))
            self.assertTrue(pd.isna(resultat_median[key]))
            self.assertTrue(pd.isna(resultat_std[key]))


if __name__ == '__main__':
    unittest.main()

        






