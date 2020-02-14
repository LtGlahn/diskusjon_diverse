#/bin/bash 
# Leser loggfil fra FME, plukker ut http kall som handler om oppslag på veglenke (v2) og veglenkesekvens (v3) og pynter litt  
# grep "HTTP transfer summary" data/opp*.log | grep veglenke | cut -d":" -f6,10-11 > data/fmekall_veglenke.log
# grep "HTTP transfer summary" data13februar/*.log | grep veglenke | cut -d":" -f6,10-11 > data13februar/fmekall_veglenke.log
grep "HTTP transfer summary" data_fylke15viatech/*.log | grep veglenke | cut -d":" -f6,10-11 > data_fylke15viatech/fmekall_veglenke.log
