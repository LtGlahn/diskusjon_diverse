# Implementerer innloggingsrituale LES som beskrevet på 
# https://nvdbapilesv3.docs.apiary.io/#reference/0/autentisering/innlogging 
# 
# Mer detaljer om SVV pålogging
# https://atlas-docs.atlas.vegvesen.no/atlas-dokumentasjon/latest/tjenester/autentisering.html 

import requests
#      https://nvdbapiles-v3.test.atlas.vegvesen.no/   
url = 'https://nvdbapiles-v3.test.atlas.vegvesen.no/auth/login'
body = {'username': 'jajens', 'password': '*****', 'user_type': 'employee'}
headers = {'Content-Type': 'application/json'}

r = requests.post( url, json=body, headers=headers) 

token = r.json() 

url2 = 'https://nvdbapiles-v3.test.atlas.vegvesen.no/vegobjekter/905'
headers2 = {  'Authorization' :  'Bearer ' + token['idToken'], 'X-Client' : 'jajens@vegvesen.no' } 

r2 = requests.get( url2, headers=headers2 )


