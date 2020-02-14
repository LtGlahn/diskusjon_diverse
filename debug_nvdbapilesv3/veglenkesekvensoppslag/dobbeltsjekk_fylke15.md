# Dobbeltsjekk av kall mot `veg` - endepunkt som feiler

Vår leverandør Viatech har levert liste over kall mot `veg` som feiler 
for fylke 15, men som er gyldige vegreferanseoppslag. 

Jeg stusser litt på deres konklusjoner, og mistenker kanskje at 
de har brukt en tidligere versjon av datasettet, hvor disse manglene
definitivt var til stede. Jeg må imidlertid sjekke litt grundigere
for å finne ut hvordan dette henger sammen. 

Datagrunnlag i mappen `data_fylke15viatech`

Viatech rapporterer om  1952 *tomme celler* i data jeg har sendt dem for fylke 15. I FME-loggene for fylke 15 sendt den 13. februar finner jeg imidlertid 488 feilsituasjoner, fordelt likt på V2 og V3. 

```
In [15]: %run analyserlogg_dobbeltsjekkfeil.py
Åpner FME loggfil oppsummering data_fylke15viatech/fmekall_veglenke.log 
Antall feil V2 244 / 10842 Feilrate= 2  %
Antall feil V3 244 / 10842 Feilrate= 2  %
Antall kall som lykkes i den ene Api-versjonen men feiler i den andre 0
Antall feilsituasjoner vi prøvde om igjen med SUKSESS 0 / 488 0 %
Antall feilsituasjoner som fremdeles feiler 488 / 488 100 %
```

# Opppsummering, alle fylker 

Her er for øvrig min nyeste sjekk av de veglenkeoppslagene som feiler i datasettet `data13februar` (gamle vegreferanser fra Viatech som skulle oppfriskes med riktig stedfesting (per angitt dato) og nye 
vegreferanseverdier). Datagrunnlag i mappen `data13februar`


```
Antall feil V2 8261 / 195547 Feilrate= 4  %
Antall feil V3 8241 / 195547 Feilrate= 4  %
Antall kall som lykkes i den ene Api-versjonen men feiler i den andre 112
Antall feilsituasjoner vi prøvde om igjen med SUKSESS 0 / 16502 0 %
Antall feilsituasjoner som fremdeles feiler 16502 / 16502 100 %
```