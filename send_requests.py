import requests
import time

def send_get_request(URL):
    while True:
        try:
            r = requests.get(URL)
            if r.status_code not in [200]:
                time.sleep(1)
            else:
                break
        except requests.exceptions.ConnectionError:
            pass
    return r