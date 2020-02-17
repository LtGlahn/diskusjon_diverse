# Feilstatistikk, V3

Her går jeg gjennom noen feil som var hyppige i tidlig fase av NVDB api V3. Repos oppdateres etter hvert som feilene rettes. 


## [Uthenting av vegobjekter gir manglende geometri og vegsystemreferanse på mange av objektene](./vegobjekter/readme.md) Ignorerbar? 

Undersøkelser så langt (sammenligne uthenting av data med samme filter fra V2 og V3) tyder på at manglende geometri i V3-spørringe er objekter som ikke skulle vært med i datauttaket, og derfor kan ignoreres. **Vi trenger mer robust statistikk før vi kan konkludere med dette!**

## [Gyldige oppslag på veglenkeposisjon i V2 feiler i V3](./veglenkesekvensoppslag/readme.md) FIKSA 


## [Meter telles feil](./metreringsretning/readme.md)


