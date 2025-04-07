import pandas as pd

class Statistiske_maal():
    def __init__(self):
        pass 
    
    '''
    def gjennomsnitt(self,df):
        tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
        data = []
        for start_år,slutt_år in tids_intervaller:
            gjennomsnitt = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].mean()
            data.append(round(float(gjennomsnitt), 2))
        gjennomsnitt_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].mean()
        data.append(round(float(gjennomsnitt_1980_2020), 2))
        return data


    def median(self,df):
        tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
        data = []
        for start_år,slutt_år in tids_intervaller:
            median = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].median().round(2)
            data.append(round(float(median), 2))
        median_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].median().round(2)
        data.append(round(float(median_1980_2020), 2))
        return data
    
    def standardavvik(self,df):
        
        #Henter ut verdiene gruppert på årstall
        fra_1980_1989 = df[(df["year"] >= 1980) & (df["year"] <= 1989)]
        fra_1990_1999 = df[(df["year"] >= 1990) & (df["year"] <= 1999)]
        fra_2000_2009 = df[(df["year"] >= 2000) & (df["year"] <= 2009)]
        fra_2010_2020 = df[(df["year"] >= 2010) & (df["year"] <= 2020)]

        fra_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]

        #Utregning av standardavvik i de ulike tiårene
        standardavvik_1980_1989 = fra_1980_1989.select_dtypes(include="number").std()
        standardavvik_1990_1999 = fra_1990_1999.select_dtypes(include="number").std()
        standardavvik_2000_2009 = fra_2000_2009.select_dtypes(include="number").std()
        standardavvik_2010_2020 = fra_2010_2020.select_dtypes(include="number").std()

        standardavvik_1980_2020 = fra_1980_2020.select_dtypes(include="number").std()

        
        data_std = [standardavvik_1980_1989,standardavvik_1990_1999,standardavvik_2000_2009,standardavvik_2010_2020,standardavvik_1980_2020]

        return data_std
'''
    

    def gjennomsnitt(self,df):
            tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
            data = []

            for start_år,slutt_år in tids_intervaller:
                gjennomsnitt = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].mean()
                data.append(round(float(gjennomsnitt), 2))

            gjennomsnitt_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].mean()
            data.append(round(float(gjennomsnitt_1980_2020)))


            return data
        
        
    def median(self,df):
        tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
        data = []

        for start_år,slutt_år in tids_intervaller:
            median = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].median().round(2).item()
            data.append(float(round(median)))

        median_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].median().round(2).item()
        data.append(float(round(median_1980_2020)))

        return data
    

    def standardavvik(self,df):
        tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
        data = []

        for start_år,slutt_år in tids_intervaller:
            std_avvik = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].std().round(2).item()
            data.append(float(std_avvik))

        std_avvik_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].std().round(2).item()
        data.append(float(std_avvik_1980_2020))

        return data

    
    