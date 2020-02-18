import json
import sjekkmengdeuttak
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

def lastned( objtypeId, mappe, v2filter ): 

    sokv2 = nvdbapi.nvdbFagdata(objtypeId)
    sokv3 = nvdbapiv3.nvdbFagdata(objtypeId)

    # Hvilket miljø bruker vi?
    # sokv2.apiurl = 'https://www.test.vegvesen.no/nvdb/api/v2'
    # sokv3.miljo( 'test')
    if not( str(objtypeId) ) in mappe: 
        mappe = mappe + str( objtypeId)

    Path(mappe).mkdir(parents=True, exist_ok=True)


    sokv2.addfilter_geo(  v2filter )

    (allev2, manglerv2) = sjekkmengdeuttak.mengdeuttak( sokv2, antall=1e12)

    vref = v2filter.pop( 'vegreferanse')
    v3filter = deepcopy(v2filter )
    if vref: 
        v3filter['vegsystemreferanse'] = vref

    sokv3.addfilter_geo(  v3filter )
    (allev3, manglerv3) = sjekkmengdeuttak.mengdeuttak( sokv3, antall=1e12)

    oo = '_' + str( objtypeId ) + '_' vref 

    with open( mappe + 'mangler_geometriv3' + oo + '.json', 'w', encoding='utf-8') as f:
        json.dump( manglerv3, f, ensure_ascii=False, indent=4)

    with open( mappe + 'mengdeuttak_v3' + oo + '.json', 'w', encoding='utf-8') as f:
        json.dump( allev3, f, ensure_ascii=False, indent=4)

    with open( mappe + 'mangler_geometriv2' + oo + '.json', 'w', encoding='utf-8') as f:
        json.dump( manglerv2, f, ensure_ascii=False, indent=4)

    with open( mappe + 'mengdeuttak_v2' + oo + '.json', 'w', encoding='utf-8') as f:
        json.dump( allev2, f, ensure_ascii=False, indent=4)


    loggtekst =  str( len( manglerv3) ) +  ' objekter av ' + str( len( allev3) ) + \
                    ' mangler geometri \nfor søket ' + str( sokv3.allfilters() ) + \
                    '\nmot ' + sokv3.apiurl 

    with open( mappe + 'logg_' + oo + '.txt', 'w', encoding='utf-8') as f3:
        f3.write( loggtekst )

    print( loggtekst)

if __name__ == "__main__":
    
    # HVa skal vi hente? 
    objtypeId = 904 

    # Hvor skal vi lagre det? 
    mappe  = 'stavanger/'

    for vref in ['E', 'R', 'F', 'K', 'P', 'S']:
        v2filter = {'kommune': 1103, 'vegreferanse': vref}
        # v3filter = {'kommune': 5001, 'vegsystemreferanse': 'K'}
        lastned( 904, mappe, v2filter)


