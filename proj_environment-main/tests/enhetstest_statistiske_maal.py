import pandas as pd
import os, sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from statistiske_maal import Statistiske_maal


class Test_Statistiske_maal(unittest.TestCase):

    def setUp(self):            #funksjonen kjører før hver test og setter opp testdata
        """
        Forbereder testmiljøet før hver enkelt testmetode kjøres.

        Fremgangsmåte:
        - Oppretter en pandas DataFrame med "year", som er en liste over årene fra 1980 til og med 2020.
          er "value" har tilhørende verdier fra 1 til 41.
        - Initialiserer et objekt av klassen "Statistiske_maal" og lagrer det som "self.sm".

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Formål:
        Sikrer at hver test starter med en fersk og identisk datastruktur, slik at testene blir isolerte og repeterbare.
        """

        # Lager testdata som dekker hele perioden 1980–2020 for å teste statistiske beregninger over tid
        data = {
            "year": list(range(1980, 2021)), # 41 år for å sikre full dekning av alle intervaller
            "value": list(range(1, 42))  # Verdier som øker jevnt for å gjøre resultatene forutsigbare
        }
        # Konverterer testdataen til en DataFrame slik at den kan brukes i statistiske analyser
        self.df = pd.DataFrame(data)

        # Initialiserer klassen som inneholder metodene vi ønsker å teste
        self.sm = Statistiske_maal()
    
    def test_gjennomsnitt(self):     
        """
        Tester funksjonen "gjennomsnitt" i klassen Statistiske_maal.

        Fremgangsmåte:
        - Kaller "gjennomsnitt" funksjonen med testdata "self.df" fra "setUp".
        - Sammenligner returverdiene for hvert tiår med manuelt beregnede forventede gjennomsnittsverdier.
        - Bruker "round" for å sikre konsistent avrunding med funksjonens resultat.

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Formål:
        Sikrer at funksjonen korrekt beregner gjennomsnittet av verdier per tiår og totalt for hele perioden 1980-2020.
        """
        result = self.sm.gjennomsnitt(self.df)

        # Funksjonen skal beregne gjennomsnitt for hvert tiår basert på "value" kolonnen.
        # Vi bruker kjente verdier slik at resultatene enkelt kan bekreftes manuelt.
        self.assertEqual(result["1980-1989"], round(sum(range(1, 11)) / 10, 2))  
        self.assertEqual(result["1990-1999"], round(sum(range(11, 21)) / 10, 2))
        self.assertEqual(result["2000-2009"], round(sum(range(21, 31)) / 10, 2))
        self.assertEqual(result["2010-2020"], round(sum(range(31, 42)) / 11, 2))
        self.assertEqual(result["Totalt"], round(sum(range(1, 42)) / 41, 2))


    def test_median(self):
        
        result = self.sm.median(self.df)
        
        #sammenligner medianen fra funksjonen med den forventede medianen
        self.assertEqual(round(result["1980-1989"], 2), 5.5)  # medianen for 1-10 er 5.5
        self.assertEqual(round(result["1990-1999"], 2), 15.5)
        self.assertEqual(round(result["2000-2009"], 2), 25.5)
        self.assertEqual(round(result["2010-2020"], 2), 36.0)
        self.assertEqual(round(result["Totalt"], 2), 21.0)


    def test_standardavvik(self):
        result = self.sm.standardavvik(self.df)

        #bruker pandas std() for å beregne standardavviken og sammenligne dette med det funksjonene regner ut
        self.assertEqual(round(result["1980-1989"], 2), round(self.df[(self.df["year"] >= 1980) & (self.df["year"] <= 1989)]["value"].std(), 2))
        self.assertEqual(round(result["1990-1999"], 2), round(self.df[(self.df["year"] >= 1990) & (self.df["year"] <= 1999)]["value"].std(), 2))
        self.assertEqual(round(result["2000-2009"], 2), round(self.df[(self.df["year"] >= 2000) & (self.df["year"] <= 2009)]["value"].std(), 2))
        self.assertEqual(round(result["2010-2020"], 2), round(self.df[(self.df["year"] >= 2010) & (self.df["year"] <= 2020)]["value"].std(), 2))
        self.assertEqual(round(result["Totalt"], 2), round(self.df[(self.df["year"] >= 1980) & (self.df["year"] <= 2020)]["value"].std(), 2))


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

        






