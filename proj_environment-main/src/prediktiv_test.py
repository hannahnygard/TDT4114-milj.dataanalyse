import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

class TrendModel:
    def __init__(self, df, x_col='year', y_col='value', test_size=0.2, random_state=42):
        self.df = df
        self.x = df[x_col].values
        self.y = df[y_col].values
        self.models = {}
        self.test_size = test_size
        self.random_state = random_state
        self.split_data()

    def split_data(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.x, self.y, test_size=self.test_size, random_state=self.random_state)
        # For plotting og prediksjon, samler vi all data sortert:
        self.x_all = np.sort(self.x)
        self.y_all = self.y[np.argsort(self.x)]

    def create_model(self, deg):
        coeffs = np.polyfit(self.x_train, self.y_train, deg=deg)
        model = np.poly1d(coeffs)
        self.models[deg] = model
        return model

    def fit_models(self, degrees=[1, 2, 3]):
        for deg in degrees:
            self.create_model(deg)

    def r2_scores(self):
        scores = {'train': {}, 'test': {}}
        for deg, model in self.models.items():
            y_train_pred = model(self.x_train)
            y_test_pred = model(self.x_test)
            scores['train'][deg] = r2_score(self.y_train, y_train_pred)
            scores['test'][deg] = r2_score(self.y_test, y_test_pred)
        return scores

    def print_r2_scores(self):
        scores = self.r2_scores()
        print("R²-scorer:")
        for deg in sorted(self.models.keys()):
            print(f"  {deg}. grads modell:")
            print(f"    Treningsdata: {scores['train'][deg]:.4f}")
            print(f"    Testdata:      {scores['test'][deg]:.4f}")

    def plot_models(self):
        X_sorted = np.sort(self.x_train)
        plt.figure(figsize=(10,6))
        plt.scatter(self.x_train, self.y_train, s=10, color='black', label="Treningsdata")
        plt.scatter(self.x_test, self.y_test, s=10, color='orange', label="Testdata")
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

    def plot_full_prediction(self, future_year, deg=1):
        if deg not in self.models:
            self.create_model(deg)
        model = self.models[deg]

        x_plot = np.linspace(self.x_all.min(), future_year, 200)
        y_pred = model(x_plot)

        plt.figure(figsize=(10, 6))
        plt.scatter(self.x_train, self.y_train, color='black', label='Treningsdata', s=10)
        plt.scatter(self.x_test, self.y_test, color='orange', label='Testdata', s=10)
        plt.plot(x_plot[x_plot <= self.x_all.max()], y_pred[x_plot <= self.x_all.max()], color='green', label=f'{deg}. grads modell')
        plt.plot(x_plot[x_plot > self.x_all.max()], y_pred[x_plot > self.x_all.max()], 'g--', label='Framtidsprediksjon')
        plt.xlabel("År")
        plt.ylabel("Verdi")
        plt.title(f"Modell og prediksjon fram til {future_year}")
        plt.legend()
        plt.grid(True)
        plt.show()

    def predict(self, year, deg=1):
        if deg not in self.models:
            self.create_model(deg)
        return self.models[deg](year)
