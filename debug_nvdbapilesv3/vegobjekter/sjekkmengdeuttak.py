"""
Rutiner for sjekk av engdeuttak fra NVDB api LES v2 og V3
  - Sjekke om noen objekter mangler "geometri" - element på rotnivå. 
    Disse rapporteres i egen liste
  - Tagge objektet med de vegkategoriene som objektet er stedfestet. 
    For å gjøre det enklere å sammenligne og etterprøve mengde-uttak 
    fra V2 og V3, samt hva vi får med direkte uthenting så 
    er denne taggen alltid sortert alfabetisk

"""
import sys
import os
import json 
import re
from copy import deepcopy
import pdb
import pandas as pd
from pathlib import Path


# Legger til nvdbap-V2 bibliotet, som ligger i undermappe relativt til
#  plasseringen til denne fila
if not [ k for k in sys.path if 'nvdbapi-V2' in k]: 
    print( "Legger NVDB api til søkestien")
    sys.path.append( os.getcwd() + '/nvdbapi-V2')

import nvdbapi 
import nvdbapiv3

def koordinatpunkt( wktstring ): 
    """
    Finner geometritype og antall koordinatpunkt i WKT streng
    """

    wkt_type = wktstring.split()[0]
    if 'Z' in wktstring[0:30].upper():
        wkt_type += ' Z'

    wktstring = re.sub( r'[a-zA-Z]+', '', wktstring)
    wktstring = re.sub( r'\(+', '', wktstring) 
    wktstring = re.sub( r'\)+', '', wktstring)
    antall_koordinatpunkt = len( wktstring.split() )

    return (wkt_type, antall_koordinatpunkt)

def veglenkestatistikk( stedfesting ):
    """
    Lager statistikk over antall lenker og utbredelse til NVDB stedfesting
    """

    antall_stedfestingelementer = len( stedfesting )
    utbredelse = None
    unike_veglenker = None 

    if 'type' in stedfesting[0]:
        if stedfesting[0]['type'] == 'Linje':
            utbredelse = sum( [ k['sluttposisjon']-k['startposisjon'] for k in stedfesting  ] ) 

        unike_veglenker = len( set(  k['veglenkesekvensid'] for k in stedfesting ))
    else: 
        unike_veglenker = len( set(  k['veglenkeid'] for k in stedfesting ))
        if 'til_posisjon' in stedfesting[0]:
            utbredelse = sum( [ k['til_posisjon']-k['fra_posisjon'] for k in stedfesting  ] ) 

    return (antall_stedfestingelementer, utbredelse, unike_veglenker)

def plukkutdata( feat, inkluderstedfesting=False): 
    """
    Drar ut de elementene vi ønsker å analysere fra et NVDB-objekt V2 / V3
    """

    if   'v3' in feat['href']: 
        apiversjon = 'v3'
    elif 'v2' in feat['href']: 
        apiversjon = 'v2'
    else:
        raise ValueError( 'Ugyldig søkeobjekt eller sok.apiurl ???')

    retur = {  'apiversjon' : apiversjon,  
                'vegobjektid' : feat['id'], 
                'href' : feat['href'], 
                'versjon' : feat['metadata']['versjon'], 
                'startdato' : feat['metadata']['startdato'], 
                'geometri' : '',
                'geometritype' : '',
                'wkt_punkt' : 0,
                'kommuner' : feat['lokasjon']['kommuner'], 
                'vegkat' : '' 
                }

    if 'geometri' in feat and 'wkt' in feat['geometri'] and len( feat['geometri']['wkt']) > 10:
        retur['geometri'] = True
        ( retur['geometritype'], retur['wkt_punkt'])  = koordinatpunkt( feat['geometri']['wkt'])
    else: 
        retur['geometri'] = False

    # V2 vegreferanser
    if 'vegreferanser' in feat['lokasjon']:
        retur['vegkat'] = ''.join( sorted( list( set( 
            [  k['kategori'] for k in feat['lokasjon']['vegreferanser'] if 'kategori' in k ] ) ) ) )

        retur['vref'] = ','.join( sorted( [  k['kortform'] for k in feat['lokasjon']['vegreferanser'] if 'kortform' in k ] ) )

    # V3 vegsystemreferanser
    if 'vegsystemreferanser' in feat['lokasjon']:
        retur['vegkat'] = ''.join( sorted( list( set( 
            [  k['vegsystem']['vegkategori'] for k in feat['lokasjon']['vegsystemreferanser'] if 'vegsystem' in k ] ) ) ) )

        retur['vref'] = ','.join( [  k['kortform'] for k in feat['lokasjon']['vegsystemreferanser'] if 'kortform' in k ] )

    if inkluderstedfesting: 
        retur['stedfestinger'] = feat['lokasjon']['stedfestinger']

    (retur['stedfesting_antall'], retur['stedfesting_utbredelse'], retur['stedfesting_unikeid']) = veglenkestatistikk( 
                feat['lokasjon']['stedfestinger'] )

    return retur

def mengdeuttak( sok, antall=3, inkluderstedfesting=False):
    """
    Henter vegobjekter fra NVDB api og returnerer data egnet for analyse

    Hensikten er å tallfeste omfanget av mangler ved nedlasting av 
    vegobjekter fra NVDB api V3. For eksempel hvor mange vegobjekter
    som mangler `geometri`-element eller data for veg(system)referanser

    ARGUMENTS
        sok - søkeobjekt fra nvdbapi.py (v2) eller nvdbapiv3.py (v3)
              fra https://github.com/LtGlahn/nvdbapi-V2

    KEYWORDS
        antall=3 Maks antall vegobjekter som skal hentes. Veldig nyttig
                 i en utviklingsfase å begrense datamengden
        
        inkluderstedfesting=False BOOLEAN, skal vi ta med liste med 
                                            stedfesting på vegnett?

    RETURNS
        (vegobjekter, manglergeom) - Tuple med to lister med vegobjekter
            vegobjekter = liste med utdrag av verdiene, tilrettelagt for 
                            analyse
            manglergeom = Disse objektene mangler `geometri` - elementet
                         Komplette vegobjekt 
    """

    # V2 eller V3 søkeobjekt?
    if hasattr( sok, 'apiurl' ) and 'lesv3' in sok.apiurl: 
        apiversjon = 'v3'
    elif hasattr( sok, 'apiurl' ) and 'v2' in sok.apiurl: 
        apiversjon = 'v2'
    else:
        raise ValueError( 'Ugyldig søkeobjekt eller so  k.apiurl ???')

    print( 'Henter', sok.objektTypeId, 'fra', sok.apiurl,  str( sok.allfilters() ))

    resultat = []
    mangler_geometri = []
    count = 0

    feat = sok.nesteForekomst()
    while feat and count < antall:
        count += 1
        if count % 1000 == 0: 
            print( '\tHenter objekt', count, 'av', min( [antall, sok.antall ] ))

        retur = plukkutdata( feat, inkluderstedfesting=inkluderstedfesting)
        if not retur['geometri']:
            mangler_geometri.append( feat)

        resultat.append( deepcopy( retur ) )

        feat = sok.nesteForekomst()

    return (resultat, mangler_geometri)

def lastned( objtypeId, mappe, v2filter ): 

    sokv2 = nvdbapi.nvdbFagdata(objtypeId)
    sokv3 = nvdbapiv3.nvdbFagdata(objtypeId)

    # Hvilket miljø bruker vi?
    # sokv2.apiurl = 'https://www.test.vegvesen.no/nvdb/api/v2'
    # sokv3.miljo( 'test')

    Path(mappe).mkdir(parents=True, exist_ok=True)


    sokv2.addfilter_geo(  v2filter )

    (allev2, manglerv2) = mengdeuttak( sokv2, antall=1e12)

    vref = v2filter.pop( 'vegreferanse')
    v3filter = deepcopy(v2filter )
    if vref: 
        v3filter['vegsystemreferanse'] = vref

    sokv3.addfilter_geo(  v3filter )
    (allev3, manglerv3) = mengdeuttak( sokv3, antall=1e12)

    oo = '_' + str( objtypeId ) + '_' + vref 

    with open( mappe + 'mangler_geometriv3' + oo + '.json', 'w', encoding='utf-8') as f:
        json.dump( manglerv3, f, ensure_ascii=False, indent=4)

    with open( mappe + 'mengdeuttak_v3' + oo + '.json', 'w', encoding='utf-8') as f:
        json.dump( allev3, f, ensure_ascii=False, indent=4)

    with open( mappe + 'mangler_geometriv2' + oo + '.json', 'w', encoding='utf-8') as f:
        json.dump( manglerv2, f, ensure_ascii=False, indent=4)

    with open( mappe + 'mengdeuttak_v2' + oo + '.json', 'w', encoding='utf-8') as f:
        json.dump( allev2, f, ensure_ascii=False, indent=4)


    minlogg = sammenlign( allev3, allev2, sokefilter=v3filter )

    print( minlogg )
    return minlogg 

def sammenlign( v3data, v2data, sokefilter='' ):

    sokefilter = str( sokefilter )

    v3data = pd.DataFrame( v3data)
    v2data = pd.DataFrame( v2data )

    # Mengdehåndtering (set) 
    v2mengde = set( v2data['vegobjektid'].tolist())
    v3gyldig = set( v3data[   v3data['geometri']]['vegobjektid'].tolist())
    v3ugyldig = set( v3data[ ~v3data['geometri']]['vegobjektid'].tolist())   

    diff_2_gyldig3      = len(v2mengde-v3gyldig)
    diff_gyldig3_2      = len(v3gyldig-v2mengde)
    overlapp_ugyldig3_2 = len( v3ugyldig & v2mengde)

    retur = []
    if diff_2_gyldig3 > 0: 
        retur.append( 'FEiL: ' + str( diff_2_gyldig3 ) + 
            ' objekter finnes i v2-søk, men ikke i V3-søk ' + sokefilter )
    
    if diff_gyldig3_2 > 0:
        retur.append ( 'FEiL: ' + str( diff_gyldig3_2) + \
            ' gyldige objekter i v3-søk som ikke finnes i v2-søk ' + sokefilter )

    if overlapp_ugyldig3_2 > 0:
        retur.append( 'FEiL: ' + str( overlapp_ugyldig3_2 ) + \
            ' ugyldige objekter i v3-søk som finnes i v2-søk ' + sokefilter  ) 

    if len( retur ) == 0: 
        retur.append( 'GODKJENT Søk mot V3 ga ' +  str( len( v3gyldig)) + \
        ' gyldige og ' + str( len( v3ugyldig )) + ' ugyldige objekter ' + \
                                                            sokefilter )

    return retur