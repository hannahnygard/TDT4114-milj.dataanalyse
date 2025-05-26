import ipywidgets as widgets
from IPython.display import clear_output, display

class DataRensWidget:
    def __init__(self, data_rens_instans, df_urenset):
        '''
        Oppstart av objekt i klassen

        Parametere:
        -En renset dataframe, instand fra klassen DataRens
        -En urenset (manipulert) dataframe, instans fra klassen DataManipulering
        '''
        self.data_rens = data_rens_instans
        self.df_urenset = df_urenset
        
        self.metode_dropdown = widgets.Dropdown(
            options=[
                ('Gjennomsnitt', 'mean'), 
                ('Median', 'median'), 
                ('Interpolering', 'interpolate')
                ],
            value='mean', #setter gjennomsnitt som default
            description='Fyll manglende med:',
        )

        # Kjør-knapp og output
        self.kjør_knapp = widgets.Button(description="Rens data")
        self.output = widgets.Output()

         # Bruk on_click, men sørg for å ikke koble opp flere ganger
        self.kjør_knapp.on_click(self.kjør_rensing)

         # Intern flagg for å holde styr på om rensing allerede er gjort
        self.already_clicked = False




    def kjør_rensing(self, _):
        '''
        Renser data i dataframe ved å fylle ut mnglende verdi med valgt valg
        Viser resultat i en jupyter widget
        
        Parametere: ingen
        '''
        with self.output:
            clear_output(wait=True)  # Tøm ut tidligere output
            df = self.df_urenset.copy()
            metode = self.metode_dropdown.value
            
            if metode == 'mean':
                fyll_verdi = df['value'].mean()
                df['value'] = df['value'].fillna(fyll_verdi)
                print("Erstattet manglende verdier med gjennomsnitt", fyll_verdi)
            elif metode == 'median':
                fyll_verdi = df['value'].median()
                df['value'] = df['value'].fillna(fyll_verdi)
                print("Erstattet manglende verdier med median", fyll_verdi)
            elif metode == 'interpolate':
                df['value'] = df['value'].interpolate()
                print("Erstattet manglende verdier med interpolering")
            
            self.data_rens.plot_manglende_data(self.df_urenset, df)
            display(df.head())

    def vis(self):
        '''
        Viser brukergrensesnittet for datarensing 
        Returnerer None, kjører en display
        '''
        clear_output(wait=True)  
        display(self.metode_dropdown, self.kjør_knapp, self.output)