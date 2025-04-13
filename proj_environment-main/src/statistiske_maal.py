import pandas as pd

class Statistiske_maal():
    def __init__(self):
        pass 
    

    def gjennomsnitt(self,df):
            tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
            data = {}

            for start_år,slutt_år in tids_intervaller:
                gjennomsnitt = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].mean()
                data[f"{start_år}-{slutt_år}"] = round(gjennomsnitt, 2)

            gjennomsnitt_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].mean()
            data[f"Totalt"] = round(gjennomsnitt_1980_2020,2)


            return data
        
        
    def median(self,df):
        tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
        data = {}

        for start_år,slutt_år in tids_intervaller:
            median = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].median()
            data[f"{start_år}-{slutt_år}"] = round(median, 2)

        median_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].median()
        data[f"Totalt"] = round(median_1980_2020, 2)

        return data
    

    def standardavvik(self,df):
        tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
        data = {}

        for start_år,slutt_år in tids_intervaller:
            std_avvik = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].std()
            data[f"{start_år}-{slutt_år}"] = round(std_avvik,2)

        std_avvik_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].std()
        data["Totalt"] = round(std_avvik_1980_2020,2)

        return data

    
    