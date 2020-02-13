"""
Knar på logger fra FME, som først har vært knadd med bash-kommando 
grep "HTTP transfer summary" data/opp*.log | grep veglenke | cut -d":" -f6,10-11 > data/fmekall_veglenke.log

og som er på formatet: 
 200, download size: 'https://www.vegvesen.no/nvdb/api/v2/veg?veglenke=0.94578140234375%401126283'
 200, download size: 'https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0.94578140234375%401126283'
 200, download size: 'https://www.vegvesen.no/nvdb/api/v2/veg?veglenke=0.18194222886550568%401125762'
 200, download size: 'https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0.18194222886550568%401125762'
 200, download size: 'https://www.vegvesen.no/nvdb/api/v2/veg?veglenke=0.31329577481823057%401125762'
 200, download size: 'https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0.31329577481823057%401125762'
 200, download size: 'https://www.vegvesen.no/nvdb/api/v2/veg?veglenke=0.75321960592743409%401125762'
 200, download size: 'https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0.75321960592743409%401125762'
 200, download size: 'https://www.vegvesen.no/nvdb/api/v2/veg?veglenke=0.99786547288010718%401125762'
 200, download size: 'https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0.99786547288010718%401125762'


 Tallet 200 antyder suksuess, alt annet er feil. 

 Denne rutina løper gjennom alle linjene og teller opp suksess og feil for hhv NVDB api V2 og V3. 


"""
import requests


def parselinje( linje ): 
    """
    Dekoder en linje på formen 
     200, download size: 'https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0.99786547288010718%401125762'

    og returnerer en dictionary med følgende komponenter: 
        { 'status' : 200, 
            'url' : 'https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0.99786547288010718@1125762',
            'kortform' :  '0.99786547288010718@1125762'
            'veglenke' : 1125762, 
            'posisjon' : 0.997865479, # Rundet av til 8 siffer
            'apiversjon' : 'v3', 
            'endepunkt' :   'https://www.vegvesen.no/nvdb/api/v3/veg'
        }
    """

    linje = linje.replace( '%40', '@')
    status = int( linje.split(',')[0] )
    url = linje.split("'")[1] 
    urlbiter= url.split( '?')
    if 'v2' in urlbiter[0]: 
        apiversjon = 'v2'
    elif 'v3' in urlbiter[0]:
        apiversjon = 'v3'
    else: 
        apiversjon = ''

    kortform = urlbiter[1].split('=')[1]

    return { 'status' : status, 
            'url' : url,
            'kortform' :  '0.99786547288010718@1125762',
            'veglenke' : int( kortform.split('@')[1]  ), 
            'posisjon' : float(  kortform.split('@')[0]  ),
            'apiversjon' : apiversjon, 
            'endepunkt' :  urlbiter[0]
        }

if __name__ == "__main__":
    # r = parselinje( "200, download size: 'https://www.vegvesen.no/nvdb/api/v3/veg?veglenkesekvens=0.99786547288010718%401125762'")
    tell_suksessv2 = 0
    tell_suksessv3 = 0
    tell_feilv2 = 0
    tell_feilv3 = 0

    data = []

    f = open( 'data13februar/fmekall_veglenke.log')
    for linje in f: 
        # rad = parselinje( f.readline() )
        rad = parselinje( linje )
        data.append( rad )
        if rad['status'] == 200 and rad['apiversjon'] == 'v2': 
            tell_suksessv2 += 1 
        elif rad['status'] == 200 and rad['apiversjon'] == 'v3': 
            tell_suksessv3 += 1 
        elif rad['apiversjon'] == 'v2':
            tell_feilv2 += 1
        elif rad['apiversjon'] == 'v3':
            tell_feilv3 += 1
        else: 
            print( 'ALVORLIG FEIL', rad)
    
    f.close()
    totaltv2 = tell_feilv2 + tell_suksessv2
    totaltv3 = tell_feilv3 + tell_suksessv3
    if totaltv2 == 0: 
        feilratev2 = 0
    else: 
        feilratev2 = round( 100 * tell_feilv2 / totaltv2  ) 

    if totaltv3 == 0:
        feilratev3 = 0
    else: 
        feilratev3 = round( 100 * tell_feilv3 / totaltv3  )

    print( 'Antall feil V2', tell_feilv2, '/', totaltv2, 'Feilrate=', feilratev2, ' %')
    print( 'Antall feil V3', tell_feilv3, '/', totaltv3, 'Feilrate=', feilratev3, ' %')


    # Ettergår feilene, dvs ulik status i v2 og v3
    avvik = []
    retta = 0
    # for (index, kk) in enumerate(data):

    #     if index % 2 == 0 and index+1 < len(data):
    #         kv3 = data[index+1] 
    #         if kk['status'] == 200 and kv3['status'] != 200:
    #             avvik.append( kk)
    #             avvik.append( data[index+1] )



    # for (index, kk) in enumerate(avvik):

    #     if index == 10 or index % 50 == 0: 
    #         print( 'Sjekker avvik', index, 'av', len(avvik))

    #     if index % 2 == 0 and index+1 < len(avvik):
    #         kv3 = avvik[index+1]
    #         r = requests.get( kv3['url'])
    #         if r.ok: 
    #             res = r.json()
    #             if 'vegsystemreferanse' in res.keys() and 'kortform' in res['vegsystemreferanse'].keys() and len( res['vegsystemreferanse']['kortform']) > 7:
    #                 retta += 1
    #             else: 
    #                 print( "Fikk 200 ok, men ikke gyldige data???", res)
    #         else: 
    #             r = requests.get( kk['url'])
    #             if r.ok: 
    #                 res2 = r.json()
    #                 print( 'Feiler i v3, suksess i v2:')
    #                 print( '\tSuksess', kk['url'])
    #                 print( '\tFEIL', kv3['url'])
    #             else: 
    #                 print( 'Feiler i både v2 og v3:')
    #                 print( '\t', kk['url'])
    #                 print( '\t', kv3['url'])

    # print( 'Gamle feil som er riktig nå:', retta )
