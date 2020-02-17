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

# HVa skal vi hente? 
objtypeId = 809

# Hvor skal vi lagre det? 
mappe  = 'skjermedeobjekt/'
Path(mappe).mkdir(parents=True, exist_ok=True)


# sokv2 = nvdbapi.nvdbFagdata(objtypeId)
sokv3 = nvdbapiv3.nvdbFagdata(objtypeId)

# Hvilket miljø bruker vi?
# sokv2.apiurl = 'https://www.test.vegvesen.no/nvdb/api/v2'
# sokv3.miljo( 'test')
# sokv3.apiurl = 'https://www.test.vegvesen.no/nvdb/api/v3'

# sokv2.addfilter_geo(  {'kommune': 5001, 'vegreferanse': 'K'} )
# sokv3.addfilter_geo(   {'kommune': 5001, 'vegsystemreferanse': 'K'} )

# (allev3, manglerv3) = sjekkmengdeuttak.mengdeuttak( sokv3, antall=1e12)
# (allev2, manglerv2) = sjekkmengdeuttak.mengdeuttak( sokv2, antall=1e12)

# with open( mappe + 'mangler_geometriv3.json', 'w', encoding='utf-8') as f:
#     json.dump( manglerv3, f, ensure_ascii=False, indent=4)

# with open( mappe + 'mengdeuttak_v3.json', 'w', encoding='utf-8') as f:
#     json.dump( allev3, f, ensure_ascii=False, indent=4)

# with open( mappe + 'mangler_geometriv2.json', 'w', encoding='utf-8') as f:
#     json.dump( manglerv2, f, ensure_ascii=False, indent=4)

# with open( mappe + 'mengdeuttak_v2.json', 'w', encoding='utf-8') as f:
#     json.dump( allev2, f, ensure_ascii=False, indent=4)


# loggtekst =  str( len( manglerv3) ) +  ' objekter av ' + str( len( allev3) ) + \
#                 ' mangler geometri \nfor søket ' + str( sokv3.allfilters() ) + \
#                 '\mmot ' + sokv3.apiurl 

# with open( mappe + 'logg.txt', 'w') as f3:
#     f3.write( loggtekst )

# print( loggtekst)


# sokv3.miljo( 'test')
# sokv3.apiurl = 'https://www.test.vegvesen.no/nvdb/api/v3'

dogn = sokv3.nesteForekomst()


print( '# Uten pålogging \n')
dogn = sokv3.nesteNvdbFagObjekt()
while dogn: 
    print( dogn.egenskapverdi('Navn'), dogn.egenskapverdi( 9466))  
    dogn = sokv3.nesteNvdbFagObjekt()

sokv3.refresh()
# sokv3.forbindelse.login()


print( '# MED pålogging \n')
dogn = sokv3.nesteNvdbFagObjekt()
while dogn: 
    print( dogn.egenskapverdi('Navn'), dogn.egenskapverdi( 9466))  
    dogn = sokv3.nesteNvdbFagObjekt()
