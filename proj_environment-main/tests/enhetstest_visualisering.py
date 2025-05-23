import unittest
import matplotlib.pyplot as plt
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from visualisering import Visualisering

class TestVisualiseringer(unittest.TestCase):
    def setUp(self):
        # lager testdata
        self.år = [2000, 2001, 2002]
        self.verdier = [10, 15, 12]
        self.median = 12
        self.gjennomsnitt = 12.33
        self.std = 2.5

        self.stat_gjennomsnitt = {"2000-2009": 12.33}
        self.stat_median = {"2000-2009": 12}
        self.stat_std = {"2000-2009": 2.5}


    def test_vis_statistikk_gyldig_data(self):
        # tester ut om funksjonen klarer å tegne en vanlig graf
        Visualisering.vis_statistikk(self.år, self.verdier, self.median, self.gjennomsnitt, self.std)
        plt.close('all')

    def test_visualiser_statistikk_per_tiår_gyldig_data(self):
        # tester om funksjonen klarer å tegne et søylediagram uten feil
        Visualisering.visualiser_statistikk_per_tiår(self.stat_gjennomsnitt, self.stat_median, self.stat_std)
        plt.close('all')
    
    def test_vis_statistikk_feil_datatype(self):
        # tester om funksjonen klarer å håndtere feil datatype
        with self.assertRaises(TypeError):
            Visualisering.vis_statistikk(["2000", "2001"], ["ti", "femten"])

    def test_vis_statistikk_ulik_lengde(self):
        # tester om funksjonen klarer å håndtere ulike lengder på listene
        with self.assertRaises(ValueError):
            Visualisering.vis_statistikk([2000, 2001], [10, 15, 12])

if __name__ == '__main__':
    unittest.main()
    