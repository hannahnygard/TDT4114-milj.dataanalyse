import pandas as pd

class Statistiske_maal():
    def __init__(self):
        pass 
    

    def gjennomsnitt(self,df):
        """
        Beregner gjennomsnittlig verdi for hver tiårsperiode og totalt for perioden 1980-2020.

        Funksjonen grupperer data etter fire definerte tidsintervaller som er, 1980-1989, 1990-1999,
        2000-2009 og 2010-2020. Deretter regnes gjennomsnittet av verdiene "value" for hvert intervall.
        I tillegg beregnes et samlet gjennomsnitt for hele perioden 1980-2020.

        Parametere:
        self (objekt): 
        Instansen av klassen denne metoden tilhører.
        df (pandas.DataFrame): 
        DataFrame som må inneholde kolonnene "year" og "value".

        Returnerer:
        En dict der nøklene er tidsintervaller som strenger og verdiene 
        er de avrundede gjennomsnittene for hvert intervall, samt
        en nøkkel "Totalt" for hele perioden.
        """

        # Deler inn perioden i tiår for å analysere utviklingen i gjennomsnitt over tid
        tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
        data = {}
        
        for start_år,slutt_år in tids_intervaller:
            # Finner snitt for hvert tiår for å se utvikling i gjennomsnittet
            gjennomsnitt = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].mean()
            data[f"{start_år}-{slutt_år}"] = round(gjennomsnitt, 2)

        # Beregner snitt for hele perioden for å ha noe å sammenligne med
        gjennomsnitt_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].mean()
        data[f"Totalt"] = round(gjennomsnitt_1980_2020,2)

        return data
        
        
    def median(self,df):
        """
        Beregner medianverdi for hver tiårsperiode og totalt for perioden 1980-2020.

        Funksjonen deler datasettet inn i fire definerte tidsintervaller som er 1980-1989, 1990-1999,
        2000-2009 og 2010-2020. Deretter regnes medianen av verdiene "value" for hvert intervall.
        I tillegg beregnes medianen for hele perioden 1980-2020.

        Parametere:
        self (objekt): 
        Instansen av klassen denne metoden tilhører.
        df (pandas.DataFrame): 
        DataFrame som må inneholde kolonnene "year" og "value".

        Returnerer:
        En dict der nøklene er tidsintervaller som strenger og verdiene 
        er de avrundede medianene for hvert intervall, samt 
        en nøkkel "Totalt" for hele perioden.
        """

        # Deler inn perioden i tiår for å analysere utviklingen i medianverdier over tid
        tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
        data = {}

        for start_år,slutt_år in tids_intervaller:
            # Henter medianverdien for hvert tidsintervall for å oppsummere perioden med en representativ verdi
            median = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].median()
            data[f"{start_år}-{slutt_år}"] = round(median, 2)

        # Beregner median for hele perioden for å ha en samlet oversikt
        median_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].median()
        data[f"Totalt"] = round(median_1980_2020, 2)

        return data
    

    def standardavvik(self,df):
        """
        Beregner standardavvik for hver tiårsperiode og totalt for perioden 1980-2020.

        Funksjonen deler datasettet inn i fire tidsintervaller som er 1980-1989, 1990-1999,
        2000-2009 og 2010-2020. Deretter regnes standardavviket til verdiene "value" 
        for hvert intervall. Til slutt beregnes også standardavviket for hele perioden 
        1980-2020.

        Parametere:
        self (objekt): 
        Instansen av klassen denne metoden tilhører.
        df (pandas.DataFrame): 
        DataFrame som må inneholde kolonnene "year" og "value".

        Returnerer:
        En dict der nøklene er tidsintervaller som strenger, og verdiene 
        er de avrundede standardavvikene for hvert intervall, samt
        en nøkkel "Totalt" for hele perioden.
        """

        # Deler inn perioden i tiår for å analysere utviklingen i standardavvik over tid
        tids_intervaller = [(1980, 1989), (1990, 1999), (2000, 2009), (2010, 2020)]
        data = {}

        for start_år,slutt_år in tids_intervaller:
            # Beregner standardavviket i hvert tidsintervall for å måle spredningen i verdiene
            std_avvik = df[(df["year"] >= start_år) & (df["year"] <= slutt_år)]["value"].std()
            data[f"{start_år}-{slutt_år}"] = round(std_avvik,2)
        # Regner ut standardavviket for hele perioden for å få en helhetlig forståelse av variasjonen
        std_avvik_1980_2020 = df[(df["year"] >= 1980) & (df["year"] <= 2020)]["value"].std()
        data["Totalt"] = round(std_avvik_1980_2020,2)

        return data

    
    