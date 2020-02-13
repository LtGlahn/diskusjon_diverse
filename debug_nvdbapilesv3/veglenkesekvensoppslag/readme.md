# Oppslag på `veg?` - endepunktet ~~feiler~~ feilet FIKSA 

Som et ledd i arbeid med å oversette steingamle 532 vegreferanseverdier til dagsferske veg(system)referanser, i både gammelt og nytt 
referansesystem, har jeg en stor mengde logger fra FME å grave i. Litt datamassasje og et par linjer python gir dette resultatet: 

## GAMMEL FEIL, RETTA: Oppslag mot `veg?` - endepunktet feiler på gyldige veglenker i V3. 

En viss feilrate er å forvente siden noen veglenkebiter blir historiske - nevnte jeg at dette var_steingamle_ vegreferanseverdier? Men denne statistikken lar seg vanskelig forklare 
på annen måte enn at alt for mange søk på veglenkesekvens og posisjon mot `veg?` feiler. 

| Api | Antall kall | Antall feiler  | Feilrate |
|:-:|---|---|---|
| v2 | 49278 | 2099 |  4% |
| v3 | 49278 | 4222 | 9% |

Dette er **eksakt de samme kallene** mot v2 (veglenke=<korform> og v3 (veglenkesekvens=<kortform>), hvor korform er på formen 0.5@1126283. Antall feil skulle være identisk _(eller så godt som, en viss toleranse må vi ha for  ulik hastighet på indeksering o.l)


### Eksempel 

Eksempel på feil som var før, men nå er retta: Oppslag på veglenkeposisjonen `0.99786547@1125762` gir gyldige data i v2  https://www.vegvesen.no/nvdb/api/v2/veg?veglenke=0.7564214@1060646, men feilet i 
v3 https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0.7564214@1060646. Dette oppslaget returnerer nå forventede verdier. 


## Nye data - feilen er RETTA! 

Vi fant tidligere 2123 oppslag som feilet mot NVDB api V2, men var gyldige oppslag i V2. 2121 av disse er nå gyldige oppslag i V3. 

Vi står igjen med disse to oppslagene som feiler i V3, men er gyldige i V2: 

  * Case 1:
    * Suksess i v2 https://www.vegvesen.no/nvdb/api/v2/veg?veglenke=0@1669840
    * feiler i v3 https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0@1669840
  * Case 2
    * Suksess i v2 https://www.vegvesen.no/nvdb/api/v2/veg?veglenke=0@1669840
    * Feiler i v3 https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0@1669840

# Ny test, verifisere at feilen er vekk (13.2.2020)

Jeg kjørte ymse  FME workspace på ny 12.2.2020. Disse FME workspacene gjør oppslag på eksakt samme veglenkeposisjon i V2 og V3 for å hente ut vegreferanseverdier for et punkt på vegnettet. Resultatet er ganske så oppløftende: 

```
bash$ ipython 
ipython%run analyserlogg.py
Antall feil V2 8261 / 195547 Feilrate= 4  %
Antall feil V3 8241 / 195547 Feilrate= 4  %
```

Jeg hadde kanskje forventet en lavere feilrate enn 4%, selv med utgangspunkt i flere år gamle vegreferanser (vi bruker visveginfo for å finne veglenkeposisjon for den dagen vegreferansen var gyldig). Hvis riktig så betyr det at 4% av disse punktene er historisk vegnett. 

**Men - vi har lært oss å stole på NVDB api V2**. Hvis vi synes 4% historisk vegnett er høyt så må vi heller ettergå det i detalj. **Nå er V2 og V3 enige om hvilke av  disse 195.547 veglenkeposisjonene som er gyldige, så på dette punktet friskmelder jeg NVDB api V3**. 