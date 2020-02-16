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

# Legger til nvdbap-V2 bibliotet, som ligger i undermappe relativt til
#  plasseringen til denne fila
if not [ k for k in sys.path if 'nvdbapi-V2' in k]: 
    print( "Legger NVDB api til søkestien")
    sys.path.append( os.getcwd() + '/nvdbapi-V2')

import nvdbapi 
import nvdbapiv3
from copy import deepcopy
import pdb

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
        raise ValueError( 'Ugyldig søkeobjekt eller sok.apiurl ???')

    print( 'Henter', sok.objektTypeId, 'fra', sok.apiurl,  str( sok.allfilters() ))

    resultat = []
    mangler_geometri = []
    count = 0

    feat = sok.nesteForekomst()
    while feat and count < antall:
        count += 1

        retur = plukkutdata( feat, inkluderstedfesting=inkluderstedfesting)
        if not retur['geometri']:
            mangler_geometri.append( feat)

        resultat.append( deepcopy( retur ) )

    

        feat = sok.nesteForekomst()

    return (resultat, mangler_geometri)