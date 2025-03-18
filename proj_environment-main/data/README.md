Describes the data directory and datasets

I denne mappen ligger data hentet fra frost.met.no          #HENTER VI CSV FRA ET ANNET STED?

Under ligger en beskrivelse av de ulike filene:
frost_data_nedbor og frost_data_temp;
    Her har vi hentet ut data fra frost med clientID-en lagret i en separat -.env fil (Derav *.env i gitignore). 
    Av nedbør har vi hentet ut nedbørsmengden per dag fra hele 2023. Det ble hentet ut to summer per dag, men denne dataen
    blir videre i rensingen gjort om til en verdi per dag, ved å finne gjennomsnittet av døgnverdiene per dag.
    Vi slet lenge med å hente ut nedbørdsdata fra flere år, men kom frem til at det ikke var lagret like mye fra denne stasjonen
    lenger bak i tid, og besluttet derfor å hente data fra hver dag ila. et år i stedet.

    Av temperatur har vi hentet ut homogeniserte middelverdier (altså et gjennomsnitt av døgnverdiene) i perioden 1980-2020.

    Det er verdt å nevne at dataen som er hentet fra frost allerede har blitt kvalitetssikret der fysikalske brudd og uregelmessigheter
    er korrigert, det står eksplisitt på nettsiden. Derfor er ikke dette nødvendigvis datasett med feil eller mangler, og datarensen
    vår dreier seg mer om å få finere og bedre formateringer, hente ut nøyaktig det vi vil ha, korrigere antall desimaler osv. 

frost_tabeller;
    Her fremstiller vi først den rå dataen i to tabeller. Dette er for å få en mer forståelig fremstilling av dataen. Videre er det to nye
    tabeller i en mer renset form. Over hver tabell står det skrevet hva som er justert og endret på i hvert tabell. 



VURDERINGSKRITERIER:
Oppgave 2:
1. Hvilke åpne datakilder er identifisert som relevante for miljødata, og hva er kriteriene (f.eks. kildeautoritet, datakvalitet, tilgjengelighet, brukervennlighet osv.) for å vurdere deres pålitelighet og kvalitet?
    Vi brukte i hovedsak meterologisk instututt som kilde for innhenting av miljødata. Vi ser på dette som er relevant, men først og fremst pålitelig kilde. MET og Frost skriver på nettsiden, under "What is Frost?" at datakvaliteten kontrolleres daglig, månedlig og årlig. Likevel er det verdt å trekke frem at alle målingene vi har ligger under "preformanceCategory C", som i følge Frost selv vil si at sensoren brukt for å ta målingene oppfyller kravene fra WMO og CIMO (World Meteorological Organization og Commission for Instruments and Methods of Observation), men mangler nødvendige målinger for kontroll, kalibrering og vedlikehold. Det vil si at selv om vi regner dataen som pålitelig og relativt feilfri, så er datarensen en viktig prosess for å likevel luke ut eventuelle feil. 


2. Hvilke teknikker (f.eks. håndtering av CSV-filer, JSON-data) er valgt å bruke for å lese inn dataene, og hvordan påvirker disse valgene datakvaliteten og prosessen videre?
    Vi har valgt å kun hente data via API-kall med videre lagring i JSON-filer.  


3. Dersom det er brukt API-er, hvilke spesifikke API-er er valgt å bruke, og hva er de viktigste dataene som kan hentes fra disse kildene?



