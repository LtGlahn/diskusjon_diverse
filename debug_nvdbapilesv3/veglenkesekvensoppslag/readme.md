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
