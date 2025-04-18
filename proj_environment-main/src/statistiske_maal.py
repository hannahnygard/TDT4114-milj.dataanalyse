import pandas as pd

class Statistiske_maal():
    def __init__(self):
        pass 
    

    def gjennomsnitt(self,df):
            tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
            data = {}

            for start_år,slutt_år in tids_intervaller:
                gjennomsnitt = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].mean()
                data[f"{start_år}-{slutt_år}"] = round(float(gjennomsnitt), 2)

            gjennomsnitt_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].mean()
            data[f"Totalt"] = round(float(gjennomsnitt_1980_2020),2)


            return data
        
        
    def median(self,df):
        tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
        data = {}

        for start_år,slutt_år in tids_intervaller:
            median = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].median().round(2).item()
            data[f"{start_år}-{slutt_år}"] = round(float(median), 2)

        median_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].median().round(2).item()
        data[f"Totalt"] = round(float(median_1980_2020), 2)

        return data
    

    def standardavvik(self,df):
        tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
        data = {}

        for start_år,slutt_år in tids_intervaller:
            std_avvik = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].std().round(2).item()
            data[f"{start_år}-{slutt_år}"] = float(std_avvik)

        std_avvik_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].std().round(2).item()
        data["Totalt"] = float(std_avvik_1980_2020)

        return data

    
    