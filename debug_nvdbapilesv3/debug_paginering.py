import requests 
import json

headers = {'accept': 'application/vnd.vegvesen.nvdb-v3-rev1+json',
 'X-Client': 'LtGlahn python',
 'X-Kontaktperson': 'jan.kristian.jensen@vegvesen.no'}

params =  {'kommune': 5001, 'vegsystemreferanse': 'K', 'inkluder' : 'alle'}

url = 'https://apilesv3.test.atlas.vegvesen.no/vegobjekter/904'
r = requests.get(  url, params=params, headers=headers  )


data = r.json()
count = 0
mangler_geometri = []

while data['metadata']['returnert'] > 0:
    count += 1 
    with open( 'debugapi_side' + str( count ) + '.json', 'w', encoding='utf-8') as f:
        json.dump( data, f, ensure_ascii=False, indent=4)


    # Fisker ut de som mangler geometri
    for feat in data['objekter']:
        if 'geometri' not in feat.keys():
            mangler_geometri.append(feat)

    
    url2 = data['metadata']['neste']['href']
    r = requests.get( url2, headers=headers)    

    data = r.json()

with open( 'mangler_geometri.json', 'w', encoding='utf-8') as f:
    json.dump( mangler_geometri, f, ensure_ascii=False, indent=4)


loggtekst =  str( len( mangler_geometri) ) +  ' objekter av ' + str( data['metadata']['antall'] ) + ' mangler geometri \nfor søket ' + url + '\nmed parametre' + str( params )
with open( 'logg.txt', 'w') as f3:
    f3.write( loggtekst )

print( loggtekst)