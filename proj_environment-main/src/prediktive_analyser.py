import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

class PrediktivModell:
    def __init__(self, df, input_col, target_col):
        '''
        Vi inisialiserer den lineære modellen

        Parametere:
            df: dataframe som inneholder både input- og målvariabel
            input_col: navnet på input-kolonnen
            target_com: navnet på mål-kolonnen

        '''

        self.df = df
        self.input_col = input_col
        self.target_col = target_col
        self.model = LinearRegression()
        self.X = df[[input_col]]
        self.y = df[target_col]
        self.trained = False

    def del_data(self, test_size=0.2, random_state=42):
        '''
        Deler datasettet inn i trenings- og testsett med train_test_split
        '''

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state
        )

    def tren_modell(self):
        '''
        Trene modellen på treningsdataen (x-train og y-train)
        setter trained = True når modellen er trent
        '''
        self.model.fit(self.X_train, self.y_train)
        self.trained = True

    def evaluer(self):
        '''
        Evaluerer modellen basert på x_test og y_test
        
        Exception reises dersom modellen ikke er trent (Dersom trained != True fra over)
        
        Returnere en orbok med MSE-score og R2-score
        '''
        if not self.trained:
            raise Exception("Modellen er ikke trent ennå.")
        y_pred = self.model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)
        return {"MSE": mse, "R2": r2}

    def prediker(self, framtidige_verdier: list):
        '''
        Tar inn en liste med fremtidige input verdier (år)
        Bruker den trente modellen til å forutsi målverdiene
        '''
        
        if not self.trained:
            raise Exception("Modellen er ikke trent ennå.")
        framtidige_df = pd.DataFrame({self.input_col: framtidige_verdier})
        return self.model.predict(framtidige_df)

    def plott(self):
        '''
        Lager et plott med treningsdata, testdata og modellens predikerte linje
        Brukes for å visuelt evaluere modellen
        
        Reiser en Exception dersom modellen ikke er trent
        '''
        if not self.trained:
            raise Exception("Modellen er ikke trent ennå.")
        
         # Lag prediksjoner for hele X (hele tidsperioden)
        y_pred_linje = self.model.predict(self.X)

        # Lag plott
        plt.figure(figsize=(10, 6))
        plt.scatter(self.X_train, self.y_train, color="blue", label="Treningsdata")
        plt.scatter(self.X_test, self.y_test, color="orange", label="Testdata")
        plt.plot(self.X, y_pred_linje, color="red", label="Modellens linje")
        plt.xlabel(self.input_col)
        plt.ylabel(self.target_col)
        plt.title(f"Lineær regresjon – verdier over tid")
        plt.legend()
        plt.grid(True)
        plt.show()


    def visualiser_prediksjon_med_test(self, framtidige_verdier: list):
        '''
        Viser samme graf som plott(), men legger til de predikterte verdiene 
        
        Tar inn en liste med de fremtidige verdien som parameter
        
        Reiser Exception dersom modellen ikke er trent 
        '''
        if not self.trained:
            raise Exception("Modellen er ikke trent ennå.")

        # Prediksjoner for historiske år (hele datasettet)
        y_pred_linje = self.model.predict(self.X)

        # Prediksjoner for fremtidige år
        framtidige_df = pd.DataFrame({self.input_col: framtidige_verdier})
        framtidige_prediksjoner = self.model.predict(framtidige_df)

        plt.figure(figsize=(10, 6))
        plt.scatter(self.X_train, self.y_train, color="blue", label="Treningsdata")
        plt.scatter(self.X_test, self.y_test, color="orange", label="Testdata")
        plt.plot(self.X, y_pred_linje, color="red", label="Modellens linje")
        plt.scatter(framtidige_df, framtidige_prediksjoner, color="green", marker='_', s=100, label="Fremtidige prediksjoner")
        plt.xlabel(self.input_col)
        plt.ylabel(self.target_col)
        plt.title(f"Prediksjon av verdier for fremtidige år ({framtidige_verdier[0]}–{framtidige_verdier[-1]})")
        plt.legend()
        plt.grid(True)
        plt.show()

    
    @staticmethod
    def plotte_prediksjoner_samme_plot(framtidige_år, prediksjoner_dict):
        """
        Plotter flere sett med prediksjoner i samme graf.

        Parametere:
        - framtidige_år: liste med årstall
        - prediksjoner_dict: dict med predikasjonene som er funnet
        """
        plt.figure(figsize=(15, 7))

        for navn, prediksjoner in prediksjoner_dict.items():
            plt.plot(framtidige_år, prediksjoner, marker='o', label=navn)

        plt.xticks(framtidige_år, rotation=45)  # Legg til denne linjen for å vise alle år
        plt.xlabel("År")
        plt.ylabel("Predikert verdi")
        plt.title("Fremtidige prediksjoner for flere miljøvariabler")
        plt.legend()
        plt.grid(True)
        plt.show()


