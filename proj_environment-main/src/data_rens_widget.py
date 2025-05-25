import ipywidgets as widgets
from IPython.display import clear_output, display

class DataRensWidget:
    def __init__(self, data_rens_instans, df_urenset):
        self.data_rens = data_rens_instans
        self.df_urenset = df_urenset
        
        self.metode_dropdown = widgets.Dropdown(
            options=[
                ('Gjennomsnitt', 'mean'), 
                ('Median', 'median'), 
                ('Interpolering', 'interpolate')
                ],
            value='mean',
            description='Fyll manglende med:',
        )

        # Kjør-knapp og output
        self.kjør_knapp = widgets.Button(description="Rens data")
        self.output = widgets.Output()

        # Sørg for at knappen ikke dobbelkobles
        if not hasattr(self.kjør_knapp, '_click_callback_added'):
            self.kjør_knapp.on_click(self.kjør_rensing)
            self.kjør_knapp._click_callback_added = True


    def kjør_rensing(self, _):
        with self.output:
            clear_output(wait=True)  # Tøm ut tidligere output
            df = self.df_urenset.copy()
            metode = self.metode_dropdown.value
            
            if metode == 'mean':
                fyll_verdi = df['value'].mean()
                df['value'] = df['value'].fillna(fyll_verdi)
                print("Erstattet manglende verdier med gjennomsnitt")
            elif metode == 'median':
                fyll_verdi = df['value'].median()
                df['value'] = df['value'].fillna(fyll_verdi)
                print("Erstattet manglende verdier med median")
            elif metode == 'interpolate':
                df['value'] = df['value'].interpolate()
                print("Erstattet manglende verdier med interpolering")
            
            self.data_rens.plot_manglende_data(self.df_urenset, df)
            display(df.head())

    def vis(self):
        clear_output(wait=True)  # NY LINJE
        display(self.metode_dropdown, self.kjør_knapp, self.output)