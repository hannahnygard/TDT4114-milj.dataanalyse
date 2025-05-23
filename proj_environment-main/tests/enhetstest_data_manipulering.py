import unittest
from unittest.mock import patch
import pandas as pd
import sys
import os

# Gjør det mulig å importere DataManipulering fra src-mappen ved å legge til src i søkestien.
# Dette er nødvendig for at testmodulen skal kunne finne og bruke klassen vi ønsker å teste.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_manipulering import DataManipulering

class TestDataManipulering(unittest.TestCase):

    def setUp(self):
        """
        Setter opp testmiljøet før hver testmetode kjøres.

        Oppretter en test-DataFrame med årene 1980-2020 og tilhørende verdier fra 0 til 40. 
        Lager også en instans av klassen DataManipulering som skal testes.
        
        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Denne metoden kjøres automatisk før hver testmetode i klassen.
        """
        # Lager DataFrame med år 1980–2020 og verdier 0–40 for å teste funksjonalitet på et kjent og kontrollert datasett
        self.df = pd.DataFrame({
            "referenceTime": pd.date_range(start="1980", periods=41, freq="YE"),
            "value": list(range(41))
        })
        # Gjør om "refranceTime" til "year" slik at analyse og gruppering kan gjøres på årsnivå
        self.df["year"] = self.df["referenceTime"].dt.year
        # Oppretter et objekt av DataManipulering for å kunne bruke metodene i klassen
        self.dm = DataManipulering()

    @patch("random.choice", return_value=1980) # Gir en bestemt verdi "1980" til random funksjonen, som hjelper oss videre i koingen
    def test_fjern_verdi_for_tilfeldig_aar(self, mock_choice):
        """
        Tester at en tilfeldig valgt verdi blir fjernet, som vil vises i from av NaN i DataFrame.

        Ved hjelp av mocking blir året 1980 alltid valgt som tilfeldig år. 
        Verifiserer at verdien for 1980 er satt til NaN i den returnerte DataFrame-en.
    
        Parametere:
        self (objekt): 
        Instansen av klassen denne metoden tilhører.
        mock_choice (Mock): 
        Mock-objekt som erstatter random.choice midlertidig.
        """
        # Bruker funksjonen som setter verdien til None for et tilfeldig år, for å teste hvordan systemet håndterer manglende data.
        df_resultat = self.dm.fjern_verdi_for_tilfeldig_aar(self.df.copy())

        # Filtrerer ut raden for 1980 for å kunne undersøke om verdien er blitt satt til NaN
        rad_1980 = df_resultat[df_resultat["year"] == 1980]

        # Sjekker at "value" feltet for 1980 faktisk er manglende, som bekreftelse på at funksjonen virker etter hensikten.
        self.assertTrue(rad_1980["value"].isnull().any())

    @patch("random.choice", return_value=1990) # Gir en bestemt verdi "1990" til random funksjonen, som hjelper oss videre i kodingen
    def test_legg_til_duplikater_for_tilfeldig_aar(self, mock_choice):
        """
        Tester at en duplikat av en rad blir korrekt lagt til for et tilfeldig valgt år.

        Mocking sikrer at året 1990 alltid velges. Verifiserer at det finnes to rader 
        for 1990 i den returnerte DataFrame-en, og at total lengde øker med en.
    
        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.
        mock_choice (Mock): 
        Mock-objekt som erstatter random.choice midlertidig.
        """

        # Sikrer at metoden legger til en ekstra rad for ett tilfeldig år, slik at duplikater kan håndteres senere
        df_resultat = self.dm.legg_til_duplikater_for_tilfeldig_aar(self.df.copy())

        # Bekrefter at det tilfeldige året 1990 nå har to rader, noe som viser at duplikatet faktisk er lagt til
        antall_1990 = df_resultat[df_resultat["year"] == 1990].shape[0]
        self.assertEqual(antall_1990, 2)

        # Verifiserer at totalantallet rader har økt med en, som forventet etter å ha lagt til en duplikat
        self.assertEqual(len(df_resultat), len(self.df) + 1)

if __name__ == "__main__":
    unittest.main()
