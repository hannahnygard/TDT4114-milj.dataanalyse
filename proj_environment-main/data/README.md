Describes the data directory and datasets

I denne mappen ligger data hentet fra frost.met.no          

Under ligger en beskrivelse av de ulike filene:
frost_data_nedbor, frost_data_temp og frost_data_lufttrykk;
    Her har vi hentet ut data fra frost med clientID-en lagret i en separat -.env fil (Derav *.env i gitignore). 
    Av nedbør har vi hentet ut nedbørsmengden per dag fra hele 2023. Det ble hentet ut to summer per dag, men denne dataen
    blir videre i rensingen gjort om til en verdi per dag, ved å finne gjennomsnittet av døgnverdiene per dag.
    Vi slet lenge med å hente ut nedbørdsdata fra flere år, men kom frem til at det ikke var lagret like mye fra denne stasjonen
    lenger bak i tid, og besluttet derfor å hente data fra hver dag ila. et år i stedet.

    Av temperatur har vi hentet ut homogeniserte middelverdier (altså et gjennomsnitt av døgnverdiene) i perioden 1980-2020.

    Av lufttrykk har vi hentet ut lufttrykk målt fra havnivå, men det ble her hentet ut flere målinger gjort per dag. For å samle disse valgte vi å finne gjennomsnittet, og bruke denne verdien som dagsverdien, for hele 2023.

    Det er verdt å nevne at dataen som er hentet fra frost allerede har blitt kvalitetssikret der fysikalske brudd og uregelmessigheter
    er korrigert, det står eksplisitt på nettsiden. Derfor er ikke dette nødvendigvis datasett med feil eller mangler, og datarensen
    vår dreier seg mer om å få finere og bedre formateringer, hente ut nøyaktig det vi vil ha, korrigere antall desimaler osv. 

frost_tabeller;
    Her fremstiller vi først den rå dataen i to tabeller. Dette er for å få en mer forståelig fremstilling av dataen. Videre er det to nye
    tabeller i en mer renset form. Over hver tabell står det skrevet hva som er justert og endret på i hvert tabell. 

lufttrykk_tabeller;
    I denne notebooken skjer det flere operasjoner. Først hentes innholdet fra JSON-filen ut og lagres i en database (frost_Database.db). Videre hentes all dataen fra databasen (med SELECT *) og konverterer til en dataframe. Så henter vi ut dataen vi faktisk trenger som fremstilles i en ny tabell, altså dataen for tid og verdi, før dataen til slutt renses. Som med tabellene over står det skrevet over tabellen på hvilken måte dataen er renset. 


--------------------------------------------------------------------------------------------------------
VURDERINGSKRITERIER:
Oppgave 2:
1. Hvilke åpne datakilder er identifisert som relevante for miljødata, og hva er kriteriene (f.eks. kildeautoritet, datakvalitet, tilgjengelighet, brukervennlighet osv.) for å vurdere deres pålitelighet og kvalitet?
    Vi brukte i hovedsak meterologisk instututt som kilde for innhenting av miljødata. Vi ser på dette som er relevant, men først og fremst pålitelig kilde. MET og Frost skriver på nettsiden, under "What is Frost?" at datakvaliteten kontrolleres daglig, månedlig og årlig. 
    
    Likevel er det verdt å trekke frem at alle målingene vi har ligger under "preformanceCategory C", som i følge Frost selv vil si at sensoren brukt for å ta målingene oppfyller kravene fra WMO og CIMO (World Meteorological Organization og Commission for Instruments and Methods of Observation), men mangler nødvendige målinger for kontroll, kalibrering og vedlikehold. Det vil si at selv om vi regner dataen som pålitelig og relativt feilfri, så er datarensen en viktig prosess for å likevel luke ut eventuelle feil. Trekk inn at vi fant


2. Hvilke teknikker (f.eks. håndtering av CSV-filer, JSON-data) er valgt å bruke for å lese inn dataene, og hvordan påvirker disse valgene datakvaliteten og prosessen videre?
    Vi hentet data via API-kall og lagret dem enten i JSON-filer eller i databaser med pandasSQL. JSON viste seg å være det enkleste formatet. Vi forsøkte først å lagre data i CSV-filer, men støtte på problemer da filene, til tross for .csv-endelsen, ikke oppførte seg som standard CSV-filer. Dette hindret videre behandling, og vi valgte derfor å utelukkende bruke JSON.
    JSON-formatets likhet med lister og ordbøker gjorde det enkelt å benytte teknikker vi allerede hadde lært i tidligere emner. Dette forenklet både rensing og kvalitetssikring av data, da vi kunne bruke kjente metoder. Vi vurderer at dette har hatt en positiv innvirkning på datakvaliteten, ettersom vår forståelse av verktøyene vi brukte bidro til et mer nøyaktig og pålitelig resultat.


3. Dersom det er brukt API-er, hvilke spesifikke API-er er valgt å bruke, og hva er de viktigste dataene som kan hentes fra disse kildene?
    Som nevnt er det meterologisk institutt sin API, frost, vi har benyttet oss av. Vi valgte å bruke kun denne API-en, da vi fant denne mer brukervennlig enn andre API-er vi fant på nett. Selv om den inneholdt få datafeil, har vi likevel opplevelsen av at vi har vist hvordan vi hadde håndtert det basert på det vi fant. 
    En annen grunn til at vi landet på å bruke Frost, var at det var enormt mye data å  hente her, med mange vrelementer fra mange år.



---------------------------------------------------------------------------------------------------------------------
Oppgave 3
1. Hvilke metoder vil du bruke for å identifisere og håndtere manglende verdier i datasettet?
    Vi sjekket gjennom hver rad og sjekket at hver dato/årstall har en tilhørende verdi, dette for å utelukke manglende verdier. Vi fant ingen manglende verdier, men har implementert kode for å håndtere det dersom det skulle vært noen. På samme måte som vi håndterte manglende data fra 31-12-23, ville vi nok brukt median, typetall eller gjennomsnitt for å legge til noe, men dette vil vært avhengig av situajsonen om hva som manglet.

2. Kan du gi et eksempel på hvordan du vil bruke list comprehensions for å manipulere dataene?
    Vi har brukt list comprehensions når vi gjør om alle kolonnene i lufttrykk-tabellen til strenger. JSON-normalize gjør om dataen til en todimensjonal tabell, og ved hjelp av .apply() går vi gjennom hver rad i tabellen og bruker funksjonen. Funksjonen i seg selv er en lambda-funksjon som går gjennom alle rader og konverterer eventuelle ordbøker og lister til strenger. Dette er for at vi diere skal kunne gjøre det om til pandas dataframe.

3. Hvordan kan Pandas SQL (sqldf) forbedre datamanipuleringen sammenlignet med tradisjonelle Pandas-operasjoner?
    Med pandas SQL kunne vi benytte oss av "vanlige" SQL-spørringer, noe som gjorde filtreringen av dataen betydelig mye enklere. Vi brukte SELECT for å hente ut kun de kolonnene vi trengte, og endte dermed opp en betydelig mer lesbar og intuitiv kode. Her kunne vi også skrevet SELECT-setninger for å filtrere på verdiene, eksempelvis hente ut verider over 0, men dette var ikke relevant i vårt tilfelle per nå, da vi er interesserte i å hente ut all dataen for nå. Dette er likevel noe vi kan benytte oss av senere i prosjektet, og visualisering og analyser av dataen. 

4. Hvilke spesifikke uregelmessigheter i dataene forventer du å møte, og hvordan planlegger du å håndtere dem?
    Som nevnt over er dataen fra frost relativt feilfri og av god kvalitet, noe vi var klar over da vi jobbet med dette. Vi (((MISSING VALUES))). Vi gikk også over duplikater i form av datoer for å se etter om samme data var dobbeltlagret - det fant vi ikke i noen av filene. Da vi gikk over manglende data i form av datoer, fant vi at både nedbør og lufttrykk manglet data for 31-12-23. Vi vil jo såklart ha data for hver dag i 2023, så vi valgte å løse dette ved å legge til både dagen og data, og brukte da medianen for desember måned som verdi. Vi vurderte også både gjennomsnitt og typetall, men landet på at medianen gir det mest reelle bildet på det av hensyn til ekstreme verdier. For temperaturer fant vi ingen manglende årstall, men fordi vi hentet ut den allerede utregnede års-verdien, kan vi ikke med sikkerhet si at ikke det mangler data fra noen dager. Her må vi rett og slett stole på Frost sin egen kvalitetssikring, og antar at disse veridene er representative. 


