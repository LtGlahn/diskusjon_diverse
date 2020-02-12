# Debug, noen av objektene fra NVDB api mangler stedfesting

Ved uttak fra NVDB api er det mange objekter (ca 5-10%?) som presenteres med merkverdig stedfesting
  - mangler geometri-element på rotnivå
  - tomt element `lokasjon/vegsystemreferanse`
  - hvis vi inkluderer elementet vegsegmenter så har det en snål fremstilling av tidsutviklingen til segmentert vegnett

## Fremgangsmåte

Ved kjøring av scriptet `debug_paginering` fås to typer utlisting: 
  - en komplett utlisting av alle data slik de hentes fra NVDB api, ei fil per pagineringsside
  - Utlisting av de vegobjektene som manglet `geometri` - elementet på rotnivå. 

## Stikkprøve, objekt 835716305 hentet fra atlas TEST 

Dette objektet mangler `geometri` - elementet og har en tom liste under `lokasjon/vegsystemreferanse`. 
Under `vegsegmenter` finnes kun ett element, med sluttdato=2016-05-02. 

Det virkelig snåle er at når vi inspiserer elementet direkte med objektets "href" 
https://apilesv3.test.atlas.vegvesen.no/vegobjekter/904/835716305/4 
så ser alt normalt ut. Da har objektet et gyldig geometri-element og utlisting av gyldige vegsystemreferanser under `lokasjon/vegsystemreferanser' 

Når jeg tar med vegsegmenter https://apilesv3.test.atlas.vegvesen.no/vegobjekter/904/835716305/4.json?inkluder=alle 
finner jeg tre elementer, det siste med åpen sluttdato (mangler sluttdato-element)

## Teori

Av en eller annen grunn tar ikke NVDB api alltid (5-10% av tilfellene) hensyn til den nyeste og gyldige stedfestingsinformasjonen når vegobjekter som tilfredsstiller søkekriteriet skal listes ut. 