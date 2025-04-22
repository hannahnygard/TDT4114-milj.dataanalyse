import unittest
from unittest.mock import patch
import pandas as pd
import sys
import os

# Imprtering av DataManipulering
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_manipulering import DataManipulering

class TestDataManipulering(unittest.TestCase):

    def setUp(self):
        # Lager DataFrame med år 1980–2020 og verdier 0–40
        self.df = pd.DataFrame({
            "referenceTime": pd.date_range(start="1980", periods=41, freq="YE"),
            "value": list(range(41))
        })
        # Gjør "referenceTime" til "year"
        self.df["year"] = self.df["referenceTime"].dt.year
        self.dm = DataManipulering()

    # Tester om en verdi faktisk blir fjernet
    @patch("random.choice", return_value=1980) # Gir en bestemt verdi "1980" til random funksjonen
    def test_fjern_verdi_for_tilfeldig_aar(self, mock_choice):
        df_resultat = self.dm.fjern_verdi_for_tilfeldig_aar(self.df.copy())

        rad_1980 = df_resultat[df_resultat["year"] == 1980]
        self.assertTrue(rad_1980["value"].isnull().any())

    # tester om det faktisk blir lagt til en duplikat
    @patch("random.choice", return_value=1990) # Gir en bestemt verdi "1990" til random funksjonen
    def test_legg_til_duplikater_for_tilfeldig_aar(self, mock_choice):
        df_resultat = self.dm.legg_til_duplikater_for_tilfeldig_aar(self.df.copy())

        antall_1990 = df_resultat[df_resultat["year"] == 1990].shape[0]
        self.assertEqual(antall_1990, 2)
        self.assertEqual(len(df_resultat), len(self.df) + 1)

if __name__ == "__main__":
    unittest.main()
