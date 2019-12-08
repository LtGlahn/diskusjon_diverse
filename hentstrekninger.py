"""
Henter data fra visveginfo og nytt stedfesting-endepunkt i NVDB api og tilrettelegger 
for bruk i QGIS og (geo)dataframes. 
"""
import xmltodict
import requests
import json 
import datetime

def hentvisveginfo( startEasting , startNorthing, endEasting, endNorthing, topologylevel='Overview'):
    """
    Henter strekning fra Visveginfo og returnerer liste med dictionary
    """
    url = 'https://visveginfo.opentns.org/RoadInfoService/GetRoadDataAlongRouteBetweenLocations'
    params = { 'viewDate' : str( datetime.date.today() ), 
               'TopologyLevel' : topologylevel, 
                 'startEasting' : startEasting, 
                 'startNorthing': startNorthing, 
                 'endEasting' : endEasting, 
                 'endNorthing' : endNorthing }
    r = requests.get( url, params)
    
    data = xmltodict.parse( r.text )
    
    if not 'RoadLineReference' in data['RouteWithData']['Route'].keys(): 
        return [] 
    
    
    mylist = []
    if isinstance( data['RouteWithData']['Route']['RoadLineReference'], list ): 
        for link in data['RouteWithData']['Route']['RoadLineReference']:
            mylist.append( vvisegment2dict( link ))
    else: 
        mylist.append( vvisegment2dict( data['RouteWithData']['Route']['RoadLineReference']  ) )

    return mylist

def vvisegment2dict( link):
    """
    Intern rutine  for å gjøre om visveginfo-data til håndterbar liste 
    """
    
    start = round( float( link['FromMeasure'] ), 8 )
    slutt = round( float( link['ToMeasure']   ), 8 )
    mydict = { 'vegref' : str( link['County']).zfill(2) + str( link['Municipality'] ).zfill(2) + ' ' + \
                          link['RoadCategory'].upper() + link['RoadStatus'].lower() + str( link['RoadNumber']) + \
                          'hp' + str( link['RoadNumberSegment']) + ' m' + \
                          str(link['RoadNumberSegmentStartDistance'] ) + '-' + \
                          str( link['RoadNumberSegmentEndDistance']), 
               'veglenkesekvensid' : link['ReflinkOID'], 
               'startposisjon' : start, 
               'sluttposisjon' : slutt, 
               'kortform'      : str( start ) + '-' + str( slutt ) + \
                                  '@' + str( link['ReflinkOID']), 
               'wkt'      :  link['WKTGeometry'] 
            }
    
    return mydict

def hentstrekning( startEasting , startNorthing, endEasting, endNorthing, omkrets=100):
    """
    Henter rute fra det nye stedfesting-endepunktet. Returnerer liste med en dict per segment. 
    """
    url = 'https://nvdbw01.kantega.no/nvdb/api/v3/beta/vegnett/rute'
    params = { 'start' :  str(startEasting) + ',' + str(startNorthing ), 
                'slutt' : str(endEasting)   + ',' + str(endNorthing), 
                'omkrets' : omkrets }
    r = requests.get( url, params=params )
    print( r.url )
    
    data = r.json()

    if not 'start' in data[0].keys(): 
        print( "FEIL ved henting av strekning")
        print( r.text )
        return []

    linklist = []


    start = v3punkt2dict(data[0]['start'], navn='Start' )
    slutt = v3punkt2dict(data[0]['slutt'], navn='Slutt' ) 
    
    for link in data[0]['elementer']: 
        nylenke = v3segment2dict( link )
        nylenke['start'] = start
        nylenke['slutt'] = slutt 
        linklist.append( nylenke )


    if len( linklist) == 0: 
        print( 'Ingen strekninger funnet')
        print( '\t', start['vegsystemreferanse']['kortform'], '-', slutt['vegsystemreferanse']['kortform'] ) 
        print( '\t', start['veglenkesekvens']['kortform'], '-', slutt['veglenkesekvens']['kortform'] ) 


    return linklist
    
def v3punkt2dict( punkt, navn='navn' ): 
    """
    Intern rutine, håndtere start- og endepunkt for streknngsdata nytt stedfesting-endepunkt
    """

    punkt['wkt'] = punkt['geometri']['wkt'] 
    punkt['vegref'] = punkt['vegsystemreferanse']['kortform']
    punkt['navn'] = navn
    punkt['kortform'] = punkt['veglenkesekvens']['kortform']
    
    return punkt

def v3segment2dict( link): 
    """
    Intern rutine for å håndtere strekningsdata fra nytt stedfesting-endepunkt
    """ 

    link['wkt'] = link['geometri']['wkt'] 
    link['vegref'] = link['vegsystemreferanse']['kortform']
    return link