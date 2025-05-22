import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

class TrendModel:
    def __init__(self, df, x_col='year', y_col='value'):
        self.df = df
        self.x = df[x_col].values
        self.y = df[y_col].values
        self.models = {}

    def create_model(self, deg):
        coeffs = np.polyfit(self.x, self.y, deg=deg)
        model = np.poly1d(coeffs)
        self.models[deg] = model
        return model

    def fit_models(self, degrees=[1, 2, 3]):
        for deg in degrees:
            self.create_model(deg)

    def plot_models(self):
        X_sorted = np.sort(self.x)
        plt.figure(figsize=(10,6))
        plt.scatter(self.x, self.y, s=10, color='black', label="Faktiske data")
        colors = ['red', 'green', 'blue']
        for i, deg in enumerate(sorted(self.models.keys())):
            y_pred = self.models[deg](X_sorted)
            plt.plot(X_sorted, y_pred, color=colors[i], label=f'{deg}. grads modell')
        plt.xlabel("År")
        plt.ylabel("Verdi")
        plt.title("Polynomregresjon")
        plt.legend()
        plt.grid(True)
        plt.show()

    def r2_scores(self):
        scores = {}
        for deg, model in self.models.items():
            scores[deg] = r2_score(self.y, model(self.x))
        return scores
    
    def print_r2_scores(self):
        print("R²-scorer for modellene:")
        for deg, score in self.r2_scores().items():
            print(f"  {deg}. grads modell: {score:.4f}")


    def predict(self, year, deg=1):
        if deg not in self.models:
            self.create_model(deg)
        return self.models[deg](year)

    def plot_prediction(self, future_year, deg=1):
        test_X = np.linspace(self.x.min(), future_year, 100)
        y_pred = self.predict(test_X, deg=deg)
        plt.figure(figsize=(10,6))
        plt.scatter(self.x, self.y, color='black', label='Faktiske data', s=10)
        plt.plot(test_X, y_pred, color='green', label=f'Prediksjon ({deg}. grads modell)')
        plt.xlabel("År")
        plt.ylabel("Verdi")
        plt.title(f"Prediksjon fram til {future_year}")
        plt.legend()
        plt.grid(True)
        plt.show()
