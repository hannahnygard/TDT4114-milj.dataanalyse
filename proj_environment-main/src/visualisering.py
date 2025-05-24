import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Visualisering():
    def vis_statistikk(år, verdier, median=None, gjennomsnitt=None, std=None, tittel="", y_label="Verdi"):
        """
        Lager et linjediagram med årlige verdier, samt det totale gjennomsnitter, standardavviket og medianen.
        Parametere:
        - år: liste eller array med årstall (x-verdier)
        - verdier: liste eller array med tilhørende verdier (y-verdier)
        - median: (float eller None) Median for hele perioden
        - gjennomsnitt: (float eller None) Gjennomsnitt for hele perioden
        - std: (float eller None) Standardavvik for hele perioden
        - tittel: (str) Tittel for plottet
        - y_label: (str) Y-akse etikett
        """

        if not all(isinstance(x, (int, float)) for x in verdier):
            raise TypeError("Alle verdier må være tall (int eller float).")
        
        plt.figure(figsize=(11, 7))
        plt.plot(år, verdier, marker='o', label='Årlige verdier')
        plt.title(tittel)
        plt.xlabel('År')
        plt.ylabel(y_label)


        #Tar høyde for hva som visualiseres
        if median is not None:
            plt.axhline(y=median, color="green", linestyle='--', label=f"Median ({median:.2f})")

        if gjennomsnitt is not None:
            plt.axhline(y=gjennomsnitt, color="red", label=f"Gjennomsnitt ({gjennomsnitt:.2f})")

        if gjennomsnitt is not None and std is not None:
            plt.fill_between(
                år,
                gjennomsnitt - std,
                gjennomsnitt + std,
                color='cyan',
                alpha=0.2,
                label='±1 standardavvik'
            )


        plt.grid(True)
        plt.legend()
        plt.show()





    def visualiser_statistikk_per_tiår(gjennomsnitt, median, standardavvik, tittel="Statistikk per tiår", ylabel="Verdi"):
        """
        Lager et søylediagram med gjennomsnitt, standardavvik og median per tiår.

        Parametere:
        - gjennomsnitt: dict med tiår som nøkkel og gjennomsnitt som verdi
        - median: dict med tiår som nøkkel og median som verdi
        - standardavvik: dict med tiår som nøkkel og standardavvik som verdi
        - tittel: tittel på plottet
        - ylabel: y-akse etikett
        """

        # Lager DataFrame
        df_statistikk = pd.DataFrame({
            'Tiår': gjennomsnitt.keys(),
            'Gjennomsnitt': gjennomsnitt.values(),
            'Median': median.values(),
            'Standardavvik': standardavvik.values()
        })

        sns.set_style("whitegrid")

        # Plot
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=df_statistikk, x='Tiår', y='Gjennomsnitt', hue='Tiår', palette='Blues', dodge=False)

        # Feilstolper (standardavvik)
        for i, row in df_statistikk.iterrows():
            ax.errorbar(x=i, y=row['Gjennomsnitt'], yerr=row['Standardavvik'], fmt='none', c='black', capsize=5)

        # Medianlinje
        median_all_years = df_statistikk['Median'].median()
        plt.axhline(median_all_years, color='red', linestyle='--', label=f"Median (alle tiår): {median_all_years:.2f}")

        # Median per tiår som kryss
        ax.scatter(df_statistikk.index, df_statistikk['Median'], color='red', zorder=5, label="Median per tiår", s=100, marker='X')

        # Etiketter og tittel
        plt.xlabel('Tiår')
        plt.ylabel(ylabel)
        plt.title(tittel, fontsize=14)
        plt.legend()
        plt.tight_layout()
        plt.show()



