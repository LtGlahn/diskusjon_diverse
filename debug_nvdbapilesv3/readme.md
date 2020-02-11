# Debug, noen av objektene fra NVDB api mangler stedfesting

Ved uttak fra NVDB api er det mange objekter (ca 5-10%?) som presenteres med merkverdig stedfesting
  - mangler geometri-element på rotnivå
  - tomt element `lokasjon/vegsystemreferanse`
  - hvis vi inkluderer elementet vegsegmenter så har det en snål fremstilling av tidsutviklingen til segmentert vegnett

# Fremgangsmåte

Ved kjøring av scriptet `debug_paginering` fås to typer utlisting: 
  - en komplett utlisting av alle data slik de hentes fra NVDB api, ei fil ´debugapi_sideN.json´ per pagineringsside
  - Utlisting av de vegobjektene som manglet `geometri` - elementet på rotnivå, fil ´mangler_geometri.json´ 
  - Deretter tar vi stikkprøver og gransker minst ett objekt i detalj

# Stikkprøve, objekt 835716305 hentet fra atlas TEST 

Vi plukker vilkårlig ut ett element med manglende ´geometri-element (ID=835716305) fra søket 
https://apilesv3.test.atlas.vegvesen.no/vegobjekter/904&kommune=5001&vegsystemreferanse=K
 
Dette objektet mangler `geometri` - elementet og har en tom liste under `lokasjon/vegsystemreferanse`. 
Under `vegsegmenter` finnes kun ett element, med sluttdato=2016-05-02. 

### Ulike verdier når objektet er del av en mengde (søkefilter) eller hentes direkte   

Det virkelig snåle er at når vi inspiserer elementet direkte med objektets "href" 
https://apilesv3.test.atlas.vegvesen.no/vegobjekter/904/835716305/4 
så ser alt normalt ut. Da har objektet et gyldig geometri-element og utlisting av gyldige vegsystemreferanser under `lokasjon/vegsystemreferanser' 

Når jeg tar med vegsegmenter https://apilesv3.test.atlas.vegvesen.no/vegobjekter/904/835716305/4.json?inkluder=alle 
finner jeg tre elementer, det siste med åpen sluttdato (mangler sluttdato-element)

### Objektets gyldige vegkategori (P) matcher ikke søkefilter (K) 

Den gyldige vegkategorien for objektet er P (privat veg), noe som ikke matcher søkefilteret mitt (vegsystemreferanse=K i Trondheim kommune). Men det matcher det ene historiske ´vegsegmenter´-elementet vi fikk, med sluttdato i 2016. 

### Søk på /veg - endepunktet med vegsystemreferanse og veglenkesekvens funker 

Søk på ´veg´ - endepunktet med veglenkeposisjon https://apilesv3.test.atlas.vegvesen.no/veg?veglenkesekvens=0.6@42806 eller vegsystemreferanse https://apilesv3.test.atlas.vegvesen.no/veg?vegsystemreferanse=PV8475S7D1m29&kommune=5001 ser ut til å fungere korrekt. 

