import requests
import json
import os
import time

class Device():
    def __init__(self, api_key, sku, device, deviceName):
        self.api_key = api_key
        self.sku = sku
        self.device = device
        self.deviceName = deviceName
        self.s = requests.Session()

        self.COLOR_MIN = 0
        self.COLOR_MAX = 255

        self.TEMP_MIN = 2000
        self.TEMP_MAX = 9000

        self.BRIGHTNESS_MIN = 1
        self.BRIGHTNESS_MAX = 100

        self.SENSITIVITY_MIN = 0
        self.SENSITIVITY_MAX = 100
    
    def __keep_in_bounds__(self, value, min_val, max_val):
        value = max(value, min_val)
        value = min(value, max_val)
        
        return value

    def on_off(self, state):
        options = {
            "on": 1,
            "off": 0,
        }
        url = 'https://openapi.api.govee.com/router/api/v1/device/control'
        headers = {
            'Govee-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        content = {
            "requestId": "uuid",
            "payload": {
                "sku": self.sku,
                "device": self.device,
                "capability": {
                    "type": "devices.capabilities.on_off",
                    "instance": "powerSwitch",
                    "value": options[state]
                }
            }
        }

        # response = requests.post(url=url, headers=headers, json=content)
        response = self.s.post(url=url, headers=headers, json=content)
        return response

    def gradient_toggle(self, state):
        options = {
            "on": 1,
            "off": 0,
        }
        url = 'https://openapi.api.govee.com/router/api/v1/device/control'
        headers = {
            'Govee-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        content = {
            "requestId": "uuid",
            "payload": {
                "sku": self.sku,
                "device": self.device,
                "capability": {
                    "type": "devices.capabilities.toggle",
                    "instance": "gradientToggle",
                    "value": options[state]
                }
            }
        }

        response = requests.post(url=url, headers=headers, json=content)
        return response
    
    def colorRGB(self, r, g, b):
        r = self.__keep_in_bounds__(r, min_val=self.COLOR_MIN, max_val=self.COLOR_MAX)
        g = self.__keep_in_bounds__(g, min_val=self.COLOR_MIN, max_val=self.COLOR_MAX)
        b = self.__keep_in_bounds__(b, min_val=self.COLOR_MIN, max_val=self.COLOR_MAX)
        
        value  = ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | ((b & 0xFF) << 0)
        url = 'https://openapi.api.govee.com/router/api/v1/device/control'
        headers = {
            'Govee-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        content = {
            "requestId": "uuid",
            "payload": {
                "sku": self.sku,
                "device": self.device,
                "capability": {
                    "type": "devices.capabilities.color_setting",
                    "instance": "colorRgb",
                    "value": value
                }
            }
        }

        response = requests.post(url=url, headers=headers, json=content)
        return response
    
    def colorTemperatureK(self, temp):
        temp = self.__keep_in_bounds__(temp, min_val=self.TEMP_MIN, max_val=self.TEMP_MAX)
        
        url = 'https://openapi.api.govee.com/router/api/v1/device/control'
        headers = {
            'Govee-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        content = {
            "requestId": "uuid",
            "payload": {
                "sku": self.sku,
                "device": self.device,
                "capability": {
                    "type": "devices.capabilities.color_setting",
                    "instance": "colorTemperatureK",
                    "value": temp
                }
            }
        }

        response = requests.post(url=url, headers=headers, json=content)
        return response
    
    def brightness(self, brightness):
        brightness = self.__keep_in_bounds__(brightness, min_val=self.BRIGHTNESS_MIN, max_val=self.BRIGHTNESS_MAX)
        
        url = 'https://openapi.api.govee.com/router/api/v1/device/control'
        headers = {
            'Govee-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        content = {
            "requestId": "uuid",
            "payload": {
                "sku": self.sku,
                "device": self.device,
                "capability": {
                    "type": "devices.capabilities.range",
                    "instance": "brightness",
                    "value": brightness
                }
            }
        }

        response = requests.post(url=url, headers=headers, json=content)
        return response
    
    def segment_color_setting(self, segment, rgb, brightness=None):
        r = self.__keep_in_bounds__(rgb[0], min_val=self.COLOR_MIN, max_val=self.COLOR_MAX)
        g = self.__keep_in_bounds__(rgb[1], min_val=self.COLOR_MIN, max_val=self.COLOR_MAX)
        b = self.__keep_in_bounds__(rgb[2], min_val=self.COLOR_MIN, max_val=self.COLOR_MAX)

        rgb = ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | ((b & 0xFF) << 0)
        
        url = 'https://openapi.api.govee.com/router/api/v1/device/control'
        headers = {
            'Govee-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        content = {
            "requestId": "uuid",
            "payload": {
                "sku": self.sku,
                "device": self.device,
                "capability": {
                    "type": "devices.capabilities.segment_color_setting",
                    "instance": "segmentedColorRgb",
                    "value": {
                        "segment": segment,
                        "rgb": rgb,
                    }
                }
            }
        }
            

        if brightness:
            brightness = self.__keep_in_bounds__(brightness, min_val=self.BRIGHTNESS_MIN, max_val=self.BRIGHTNESS_MAX)
            content["payload"]["capability"]["value"]["brightness"] = brightness

        response = requests.post(url=url, headers=headers, json=content)
        return response
    
    def music_setting(self, musicMode, rgb, sensitvity=None, autoColor=None):
        r = self.__keep_in_bounds__(rgb[0], min_val=self.COLOR_MIN, max_val=self.COLOR_MAX)
        g = self.__keep_in_bounds__(rgb[1], min_val=self.COLOR_MIN, max_val=self.COLOR_MAX)
        b = self.__keep_in_bounds__(rgb[2], min_val=self.COLOR_MIN, max_val=self.COLOR_MAX)

        rgb = ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | ((b & 0xFF) << 0)
        
        url = 'https://openapi.api.govee.com/router/api/v1/device/control'
        headers = {
            'Govee-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        content = {
            "requestId": "uuid",
            "payload": {
                "sku": self.sku,
                "device": self.device,
                "capability": {
                    "type": "devices.capabilities.music_setting",
                    "instance": "musicMode",
                    "value": {
                        "musicMode": musicMode,
                        "autoColor": autoColor,
                        "rgb": rgb,
                    }
                }
            }
        }

        if sensitvity:
            sensitvity = self.__keep_in_bounds__(sensitvity, min_val=self.SENSITIVITY_MIN, max_val=self.SENSITIVITY_MAX)
            content["payload"]["capability"]["value"]["sensitivity"] = sensitvity

        if autoColor:
            options = {
                "on": 1,
                "off": 0,
            }
            content["payload"]["capability"]["value"]["autoColor"] = options[autoColor]

        response = requests.post(url=url, headers=headers, json=content)
        return response
    
    def get_state(self):
        url = 'https://openapi.api.govee.com/router/api/v1/device/state'
        headers = {
            'Govee-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        content = {
            "requestId": "uuid",
            "payload": {
                "sku": self.sku,
                "device": self.device,
            }
        }

        response = requests.post(url=url, headers=headers, json=content)
        return response

    def get_scenes(self):
        url = 'https://openapi.api.govee.com/router/api/v1/device/scenes'
        headers = {
            'Govee-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        content = {
            "requestId": "uuid",
            "payload": {
                "sku": self.sku,
                "device": self.device,
            }
        }

        response = requests.post(url=url, headers=headers, json=content)
        return response
    
    def get_diys(self):
        url = 'https://openapi.api.govee.com/router/api/v1/device/diy-scenes'
        headers = {
            'Govee-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        content = {
            "requestId": "uuid",
            "payload": {
                "sku": self.sku,
                "device": self.device,
            }
        }

        response = requests.post(url=url, headers=headers, json=content)
        return response
    
class Animation(Device):
    def __init__(self, device):
        self.state = None
        self.device = device

    def goal(self, length, primary_color, secondary_color):
        t_end = time.time() + length
        sleep_time = 0.05
        while time.time() < t_end:
            self.device.colorRGB(255,0,0)
            # self.device.segment_color_setting(segment=[0,1,2,3,4,5], rgb=primary_color)
            # self.device.segment_color_setting(segment=[6,7,8,9,10,11], rgb=secondary_color)
            # time.sleep(sleep_time)
            self.device.colorRGB(0,0,255)
            # self.device.segment_color_setting(segment=[0,1,2,3,4,5], rgb=secondary_color)
            # self.device.segment_color_setting(segment=[6,7,8,9,10,11], rgb=primary_color) 
            # time.sleep(sleep_time)

class Govee():
    def __init__(self, api_key):
        self.api_key = api_key
        self.devices = self.get_devices()
    
    def get_devices(self):
        url = 'https://openapi.api.govee.com/router/api/v1/user/devices'  
        headers = {
            'Govee-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        response = requests.get(url=url, headers=headers)
        devices = []
        if response.ok:
            for device in response.json()["data"]:
                new_device = Device(api_key=self.api_key, 
                                    sku=device["sku"], 
                                    device=device["device"], 
                                    deviceName=device["deviceName"])
                devices.append(new_device)
        else:
            raise Exception("Did not return 200")
        
        return devices
    

govee = Govee(api_key='34540eff-22d0-4759-805e-09ff9d1caa84')
# man_cave_lights = govee.devices[-1]
wall_lights = govee.devices[1]

print(wall_lights.get_diys().content)
