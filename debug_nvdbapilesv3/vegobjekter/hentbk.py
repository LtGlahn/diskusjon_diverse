import json
import sys
import os
import json 
from pathlib import Path

# Legger til nvdbap-V2 bibliotet, som ligger i undermappe relativt til
#  plasseringen til denne fila
if not [ k for k in sys.path if 'nvdbapi' in k]: 
    print( "Legger NVDB api til søkestien")
    sys.path.append( os.getcwd() + '/nvdbapi-V2')

import nvdbapi 
import nvdbapiv3 
from copy import deepcopy

import sjekkmengdeuttak


if __name__ == "__main__":
    
    # HVa skal vi hente? 
    objtypeId = 904 

    # Hvor skal vi lagre det? 
    mappe  = 'stavanger' 
    mappe += '_' +  str( objtypeId) + '/'
    minlogg = []

    for vref in ['E', 'R', 'F', 'K', 'P', 'S']:
        v2filter = {'kommune': 1103, 'vegreferanse': vref}
        # v3filter = {'kommune': 5001, 'vegsystemreferanse': 'K'}
        tmp = sjekkmengdeuttak.lastned( 904, mappe, v2filter) 
        minlogg.extend( tmp)

    with open( mappe + 'logg.txt' , 'w', encoding='utf-8') as f:
        f.write( '\n'.join( minlogg ))

