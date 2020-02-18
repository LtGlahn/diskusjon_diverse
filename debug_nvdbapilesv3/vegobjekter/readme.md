# Problem: noen av objektene fra NVDB api mangler stedfesting

Ved uttak fra NVDB api er det mange objekter (ca 5-10%?) som presenteres med merkverdig stedfesting
  - mangler geometri-element på rotnivå
  - tomt element `lokasjon/vegsystemreferanse`
  - hvis vi inkluderer elementet vegsegmenter så har det en snål fremstilling av tidsutviklingen til segmentert vegnett

Derimot finner vi helt vanlige, gyldige objekter med fornuftige verdier når vi gransker ett og ett via 
`href` - lenken. Det er altså datauttak via `vegobjekter<objType.Id>`- endepunktet som feiler. 

[Mer detaljer](./stedfestingproblem.md) 

# Men - dette er til å leve med 

Ved å sammenligne likelydende søk mot NVDB api V2 og NVDB api V3 finner vi at 
**når vi fjerner objektene med tomt `geometri`-element så gir søkene mot V2 og V3 identiske resultater** 

Detaljer i diverse kode og resultatfiler her i dette reposet. P.t. har vi sammenlignet søk på 904 Bruksklasse i Stavanger kommune på 
vegkategoriene E, R, F, K, P, S. 

# Hva som bør gjøres av ytterligere undersøkelser 
  * [ ] Kjøre flere sammenligninger, for store og små områder
  * [ ] Se om det er særpreg / fellestrekk ved de vegobjektene som er problematiske 

Stikkprøver tyder på at problemet gjelder veger som var kommunalveger for noen år siden. Dvs etellerannet i 
redigeringshistorikken for kommunalveger som utløser feil når NVDB api V3 skal tolke dataene. 


