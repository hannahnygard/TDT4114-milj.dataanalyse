import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

class TrendModel:
    def __init__(self, df, x_col='year', y_col='value'):
        self.df = df
        self.x = df[x_col].values
        self.y = df[y_col].values
        self.modeller = {}

    def opprett_modell(self, grad):
        #oppretter en polynommodeller
        koeffisienter = np.polyfit(self.x, self.y, deg=grad)
        modell = np.poly1d(koeffisienter)
        self.modeller[grad] = modell
        return modell

    def tilpass_modeller(self, grader=[1, 2, 3]):
        #oppretter en modell for hver grad
        for grad in grader:
            self.opprett_modell(grad)

    def plot_modeller(self):
        #plotter alle lagrede modeller sammen med datapunktene fra dataen
        X_sorted = np.sort(self.x)
        plt.figure(figsize=(10,6))
        plt.scatter(self.x, self.y, s=10, color='black', label="Faktiske data")
        colors = ['red', 'green', 'blue']
        for i, grad in enumerate(sorted(self.modeller.keys())):
            y_pred = self.modeller[grad](X_sorted)
            plt.plot(X_sorted, y_pred, color=colors[i], label=f'{grad}. grads modell')
        plt.xlabel("År")
        plt.ylabel("Verdi")
        plt.title("Polynomregresjon")
        plt.legend()
        plt.grid(True)
        plt.show()

    def r2_scores(self):
        #regner ut r2-scoren for hver modell,
        #for å finne ut av hvilken grad som passer best 
        scores = {}
        for grad, modell in self.modeller.items():
            scores[grad] = r2_score(self.y, modell(self.x))
        return scores
    
    def print_r2_scores(self):
        #skriver ut r2-scoren for alle modeller
        print("R²-scorer for modellene:")
        for grad, score in self.r2_scores().items():
            print(f"  {grad}. grads modell: {score:.4f}")


    def prediktere(self, år, grad=1):
        #lager en prediksjon for gitt år basert på modell av ønsket grad
        if grad not in self.modeller:
            self.opprett_modell(grad)
        return self.modeller[grad](år)

    def plot_prediksjon(self, framtidig_år, grad=1):
        #plotter en prediksjon av framtidige verdier frem til et bestemt år
        test_X = np.linspace(self.x.min(), framtidig_år, 100)
        y_pred = self.prediktere(test_X, grad=grad)
        plt.figure(figsize=(10,6))
        plt.scatter(self.x, self.y, color='black', label='Faktiske data', s=10)
        plt.plot(test_X, y_pred, color='green', label=f'Prediksjon ({grad}. grads modell)')
        plt.xlabel("År")
        plt.ylabel("Verdi")
        plt.title(f"Prediksjon fram til {framtidig_år}")
        plt.legend()
        plt.grid(True)
        plt.show()
