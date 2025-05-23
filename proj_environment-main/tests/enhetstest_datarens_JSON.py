import unittest
import pandas as pd
import sys, os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_rens import DataRens


class Test_DataRens(unittest.TestCase):

    def setUp(self):
        """
        Setter opp testmiljøet før hver test i testklassen kjøres.

        Oppretter en instans av "DataRens", som inneholder metoder som skal testes.
        Det lages en "testfil.json" med en korrekt struktur som 
        etterligner et typisk datasett fra API-et eller databasen.
        JSON-filen inneholder en post med to observasjoner, begge knyttet til nedbør.

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Denne metoden kjøres automatisk før hver enkelt testmetode, slik at 
        testene har tilgang til en gyldig og konsistent testfil.
        """
        self.rens = DataRens()
        self.test_fil = os.path.join(os.path.dirname(__file__), 'testfil.json')

        # Lager en JSON-struktur med gyldig format slik at testene kan simulere ekte responsdata
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



    def test_fra_json_til_dataframe(self):
        """
        Tester funksjonen "fra_json_til_dataframe" i DataRens klassen.
        Testen bruker en forhåndsdefinert testfil som er opprettet i "setUp" med kjent struktur og innhold.

        Testen sjekker følgende:
        - At funksjonen returnerer et objekt av typen "pandas.DataFrame".
        - At antall rader i DataFrame-en er korrekt.
        - At verdien på første rad samsvarer med testdataen.

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Målet er å verifisere at JSON-filen leses riktig og at DataFrame-en 
        konstrueres korrekt fra observasjonene i filen.
        """
        
        # Bruker filen som ble opprettet i setUp for å sikre at testen har kjent og kontrollert input
        testfil_sti = self.test_fil  

        # Leser innholdet fra testfilen gjennom funksjonen som skal testes for å undersøke om den håndterer input korrekt
        df = self.rens.fra_json_til_dataframe(testfil_sti)

        # Sikrer at resultatet er en DataFrame for å bekrefte at funksjonen returnerer forventet datatype
        self.assertIsInstance(df, pd.DataFrame)  

        # Verifiserer at antall rader i resultatet samsvarer med antallet observasjoner som ble lagt inn, for å teste korrekt lesing
        self.assertEqual(len(df), 2)
    
        # Kontrollerer at verdien i første rad samsvarer med testdataen for å forsikre oss om at dataen hentes korrekt ut
        self.assertEqual(df.iloc[0]["value"], 100)



    def test_nye_nedbor_verdier(self):
        """
        Tester funksjonen "nye_nedbør_verdier" i DataRens klassen.

        Testen bruker en enkel DataFrame med to år:
        - Ett skuddår (2020) med totalverdi lik 366 mm.
        - Ett vanlig år (2021) med totalverdi lik 365 mm.

        Følgende verifiseres:
        - At kolonnen "days" blir korrekt kalkulert. Som vil si 366 for skuddår og 365 for vanlig år.
        - At kolonnen "value" som representerer gjennomsnitt per dag er riktig kalkulert til 1.0 for begge rader.
        - At kolonnen "total_values" eksisterer i resultatet.

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Målet er å bekrefte korrekt beregning av nedbør per dag og riktig håndtering av skuddår.
        """
        
        # Oppretter en DataFrame med både skuddår og vanlig år for å teste hvordan funksjonen håndterer variasjoner i antall dager per år
        df = pd.DataFrame([
            {"year": 2020, "value": 366, "unit": "mm"},  #Viser skuddår som vil hjelpe videre i koden
            {"year": 2021, "value": 365, "unit": "mm"}   #Viser vanlig år som vil hjelpe oss videre i koden
        ])
        resultat = self.rens.nye_nedbør_verdier(df)

        # Bekrefter at funksjonen beregner korrekt antall dager for et skuddår, for å sikre at årstypen blir tatt hensyn til
        self.assertEqual(resultat.loc[0, "days"], 366)
        
        # Validerer at nedbør per dag er korrekt for skuddåret, for å teste at verdi divisjonen gjøres riktig
        self.assertEqual(resultat.loc[0, "value"], 1.0)
        
        # Sikrer at beregningen også er riktig for et vanlig år, for å bekrefte konsistens i logikken
        self.assertEqual(resultat.loc[1, "value"], 1.0)
        
        # Undersøker at kolonnen som skal vise total nedbør fortsatt finnes i resultatet, for å kontrollere at ingen data går tapt i prosessen
        self.assertIn("total_values", resultat.columns)



    def test_rens_dataframe(self):
        """
        Tester funksjonen "rens_DataFrame" i DataRens klassen.
        
        Funksjonen leser inn testdata fra JSON-fil opprettet i "setUp". Før den
        konverterer JSON til DataFrame med "fra_json_til_dataframe", og renser 
        DataFrame med "rens_DataFrame".

        Testen verifiserer at:
        - Den returnerte verdien er en "pd.DataFrame".
        - DataFramen har forventet antall rader.
        - Kolonnen "value" finnes etter rensing.
        - Verdien i første rad er korrekt.

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Formål:
        Sikre at renselogikken fungerer som forventet ved å teste kolonneendringer,
        filtrering og bevaring av riktige verdier.
        """

        # Henter inn testfilen som ble opprettet i setUp for å sikre konsistent og kontrollert testgrunnlag
        testfil_sti = self.test_fil 

        # Kaller på funksjonen som konverterer JSON til DataFrame for å kunne utføre videre rensing og analyser
        df = self.rens.fra_json_til_dataframe(testfil_sti)

        # Utfører rensing av DataFrame for å fjerne unødvendige eller uønskede data før videre analyse
        renset_df = self.rens.rens_DataFrame(df)

        # Bekrefter at det rensede resultatet fortsatt er en gyldig DataFrame, for å sikre dataintegritet
        self.assertIsInstance(renset_df, pd.DataFrame)

        # Validerer at det korrekte antallet rader er bevart etter rensing, noe som indikerer at relevante data ikke har blitt fjernet
        self.assertEqual(len(renset_df), 2)

        # Kontrollerer at kolonnen "value" finnes, som en bekreftelse på at ønsket struktur i datasettet er beholdt
        self.assertIn("value", renset_df.columns)

        # Sikrer at verdien fra første observasjon er korrekt, for å teste at dataene er hentet og behandlet som forventet
        self.assertEqual(renset_df.iloc[0]["value"], 100)



    def tearDown(self):
        """
        Oppryddingsmetode som kjøres etter hver test.

        Parametere:
        self (objekt):
        Instansen av klassen denne metoden tilhører.

        Formål:
        Fjerner testfilen "self.test_fil" som ble opprettet i "setUp",
        slik at hver test kjøres med et rent utgangspunkt og unngår
        konflikt med eksisterende filer eller etterlatenskaper fra tidligere tester.

        Sikkerhet:
        Sjekker om filen eksisterer før den forsøkes slettet.
        """

        # Fjerner testfilen etter hver test for å unngå at gammel testdata påvirker resultatene i fremtidige tester
        if os.path.exists(self.test_fil):
            os.remove(self.test_fil)



if __name__ == "__main__":
    unittest.main()
