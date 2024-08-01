import requests
import json

url = f'https://openapi.api.govee.com/router/api/v1/user/devices'  
api_key = '34540eff-22d0-4759-805e-09ff9d1caa84'
device_id = '1D:89:C9:38:30:33:3E:85'

headers = {
    'Govee-API-Key': api_key,
    'Content-Type': 'application/json'
}    

   
response = requests.get(url, headers=headers)
with open('data.json', 'w') as f:
    json.dump(response.json(), f)

