import requests
import time

url = f'https://developer-api.govee.com/v1/devices/control'    
api_key = '34540eff-22d0-4759-805e-09ff9d1caa84'
device_id = '1D:89:C9:38:30:33:3E:85'
headers = {
    'Govee-API-Key': api_key,
    'Content-Type': 'application/json'
}    

content = {
    'device': device_id,
    'model': 'H610A',
    'cmd': {
        'name': 'turn',
        'value': 'on'
    }
}

start = time.time()
response = requests.put(url, headers=headers, json=content)
end = time.time()
print(end-start)
print(response.content)

