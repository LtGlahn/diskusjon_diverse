import json
import sjekkmengdeuttak
import sys
import os
import json 
from pathlib import Path
import pandas as pd

# Legger til nvdbap-V2 bibliotet, som ligger i undermappe relativt til
#  plasseringen til denne fila
if not [ k for k in sys.path if 'nvdbapi' in k]: 
    print( "Legger NVDB api til søkestien")
    sys.path.append( os.getcwd() + '/nvdbapi-V2')

import nvdbapi 
import nvdbapiv3 

# HVa skal vi hente? 
objtypeId = 938

# Hvor skal vi lagre det? 
mappe  = 'skjermedeobjekt/'
Path(mappe).mkdir(parents=True, exist_ok=True)


# sokv2 = nvdbapi.nvdbFagdata(objtypeId)
sokv3 = nvdbapiv3.nvdbFagdata(objtypeId)
sokv3.miljo( 'test')

df_opnedata = pd.DataFrame(  sokv3.to_records()  )

sokv3skjerm = nvdbapiv3.nvdbFagdata(objtypeId)
sokv3skjerm.miljo( 'test')
sokv3skjerm.forbindelse.login()

df_skjermededata = pd.DataFrame( sokv3skjerm.to_records( ))

print( 'Åpne data - skal IKKE inneholde "Graveformål"')
print( df_opnedata.dtypes )

print( '\n=====\nSkjermede data - SKAL inneholde "Graveformål')
print( df_opnedata.dtypes )


print( '\n\n')

if 'Graveformål' in df_opnedata.dtypes: 
    print( 'FEIL - åpne data har verdi for skjermet egenskaptype "Graveformål"')
else: 
    print( 'Godkjent - åpne data har ikke verdi for skjermet egenskaptype "Graveformål"')


if 'Graveformål' in df_skjermededata.dtypes: 
    print( '\nGODKJENT - vi får tilgang til skjermet egenskaptype "Graveformål" med innlogging')
else: 
    print( '\nFEIL - vi får IKKE tilgang til skjermet egenskaptype "Graveformål" med innlogging')
