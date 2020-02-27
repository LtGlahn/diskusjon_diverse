import requests

url = 'https://apilesv3.test.atlas.vegvesen.no/auth/login'
body = {'username': 'jajens', 'password': '*****', 'user_type': 'employee'}
headers = {'Content-Type': 'application/json'}


r = requests.post( url, json=body, headers=headers) 

token = r.json() 

url2 = 'https://apilesv3.test.atlas.vegvesen.no/vegobjekter/905'
headers2 = {  'Authorization' :  'Bearer ' + token['idToken'], 'X-Client' : 'jajens@vegvesen.no' } 

r2 = requests.get( url2, headers=headers2 )


