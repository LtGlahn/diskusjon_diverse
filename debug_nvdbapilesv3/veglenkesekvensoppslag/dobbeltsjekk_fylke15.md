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

### Stusser på angitte veglenkeposisjoner i fil fra Viatech 

Viatech sin fil `data_fylke15viatech/Fylke 15 - GenMethodfileFromCvs20200213_041246.txt` oppsummerer de vegsystemreferansene som mangler i 
de dataene jeg sendte dem. Her er første oppføring fra fila
```
Mangler 'ny_vegsystemreferanse_fra' for 0.63720528@2179875, ReflinkOID : 0.63720528@249525 <-> 0.68579931@249525, Org vegRef.: 1500Ev39hp16m0 - 1500Ev39hp16m30
	ny_vegsystemreferanse_fra, lesAPI :0.63720528@2179875 -> EV39 S30D1 m4834
``` 
Oppgitt vegreferanse i "Fra" - posisjon er `1500Ev39hp16m0`, skrevet som visveginfo-syntaks: `1500EV0003901600000`. I FME-loggen finner vi dette kallet til visveginfo: http://visveginfo-static.opentns.org/RoadInfoService/GetRoadReferenceForReference?roadReference=1500EV0003901600000&topologyLevel=Overview&ViewDate=2014-08-12

Som returnerer posisjon 0.63716548 (rundet av til 8 siffer) på veglenkesekvens 2179875. Dvs kortform 0.637165484709574@2179875 som gir gyldig oppslag mot NVDB api v3 
https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0.637165484709574@2179875
som gir vegsystemreferansen EV39 S30D1 m4834. 

Ut fra FME-loggen så har vi fått gyldige data _(http status kode 200, et par hundre bytes lastet ned)_ på alle kall mot nvdb api V2 og V3 `veg` - endepunktet med parameter `veglenkeposisjon=0.63716548 (eller finere) @2179875`. 

```
 bash$ grep 2179875 Metodefil_Region_MIDT_OldRef_15.log | grep status | grep 0.63716548
2020-02-13 01:30:48|  18.5|  0.0|INFORM|HTTPCaller_6(HTTPFactory): HTTP transfer summary - status code: 200, download size: '299 bytes', DNS lookup time: '1e-6 seconds', total transfer time: '0 seconds', url: 'https://www.vegvesen.no/nvdb/api/v2/veg?veglenke=0.637165484709574%402179875'
2020-02-13 01:30:48|  18.5|  0.0|INFORM|HTTPCaller_8(HTTPFactory): HTTP transfer summary - status code: 200, download size: '526 bytes', DNS lookup time: '1e-6 seconds', total transfer time: '0.063 seconds', url: 'https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0.637165484709574%402179875'
2020-02-13 01:30:49|  18.5|  0.0|INFORM|HTTPCaller_4(HTTPFactory): HTTP transfer summary - status code: 200, download size: '280 bytes', DNS lookup time: '1e-6 seconds', total transfer time: '0.031 seconds', url: 'https://www.vegvesen.no/nvdb/api/v2/veg?veglenke=0.63716548%402179875'
2020-02-13 01:30:49|  18.5|  0.0|INFORM|HTTPCaller_7(HTTPFactory): HTTP transfer summary - status code: 200, download size: '494 bytes', DNS lookup time: '1e-6 seconds', total transfer time: '0.047 seconds', url: 'https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0.63716548%402179875'
```
Jeg merker meg at posisjonen Viatech oppgir (`0.63720528`) avviker fra det jeg får manuelt her (`0.63716548`, differanse  = `0.0000398`), og som er brukt i kallene mot tjenesten. Vi pleier regne med 8 siffers presisjon i disse kallene, men i dette tilfellet påvirker ikke dette den returnerte vegsystemreferanse. Avvik på  5. siffer vil kun få betydning på de lengste veglenkene. 

En annen merknad er at det er en del duplikater i metodefil-XML'en som er utgangspunkt for vår analyse. 

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
