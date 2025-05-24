import unittest
import pandas as pd
import numpy as np
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from prediktiv_analyse import TrendModel

class TestTrendModel(unittest.TestCase):
    def setUp(self):
        #kjøres før hver test og setter opp et testdatasett
        #testdataen har en lineær sammenheng, verdien øker jevnt hver år
        self.df = pd.DataFrame({
            'year': np.arange(2000, 2010),
            'value': np.linspace(10, 20, 10)
        })
        self.model = TrendModel(self.df)


    def test_fit_models_funksjon(self):
        #tester flere funksjons-grader blir opprettet og lagret i self.models
        #testen opprettes for å bekrefte at modellen hånterer flere polynomgrader samtidig
        self.model.fit_models([1, 2, 3])
        self.assertEqual(len(self.model.models), 3)
        for deg in [1, 2, 3]:
            self.assertIn(deg, self.model.models)

    def test_predict_data(self):
        #lager en 2.grads funksjon og gjør en prediksjon for 2015
        #testen skal bekrefte at prediksjonen returnerer en tallverdi (float)
        self.model.create_model(2)
        result = self.model.predict(2015, deg=2)
        self.assertIsInstance(result, (float, np.float64))

    def test_plot_models_kjører(self):
        #lager en funksjon og plotter den, tester om plottingen vil krasje
        self.model.fit_models([1])
        try:
            self.model.plot_models()
        except Exception as e:
            self.fail(f"plot_models() krasjet med: {e}")

    def test_plot_prediction_kjører(self):
        #lager en modell og forsøker å visualisere en fremtidig prediksjon til 2015
        #tester at funksjonen kjører feilfritt (ser ikke på selve plottingen av prediksjonen)
        self.model.create_model(2)
        try:
            self.model.plot_prediction(future_year=2025, deg=2)
        except Exception as e:
            self.fail(f"plot_prediction() krasjet med: {e}")

    def test_r2_scores_beregning(self):
        #kjører fit_models og returnerer r2-scoren
        #sjekker at det finnes en score for 1.gradsfunksjon og at scoren ligger mellom 0 og 1
        self.model.fit_models([1])
        scores = self.model.r2_scores()
        self.assertIn(1, scores)
        self.assertGreaterEqual(scores[1], 0)

    def test_create_model_feil_grad(self):
        #tester om funksjonen håndterer feil datatype, ved å returnere en ValueError
        with self.assertRaises(ValueError):
            self.model.create_model('andre')

    def test_predict_feil_år(self):
        #tester om funksjonen klarer å håndtere et ugyldig år, 
        #forventes at det gir en TypeError
        self.model.create_model(1)
        with self.assertRaises(TypeError):
            self.model.predict("to tusen og ti", deg=1)


if __name__ == '__main__':
    unittest.main()

