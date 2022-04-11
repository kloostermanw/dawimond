
import requests
import json
import sys, os, time
sys.path.insert(0, os.path.abspath('..'))
from scripts.script import Script

class Service:
    # Init.
    #
    def __init__(self):
        with open('config.json') as config_file:
            conf = json.load(config_file)

        self.token = conf['token']
        self.base_url = conf['base_url']
        self.host_id = conf['host_id']
        self.develop = False
        self.config_refresh = 0

        if "develop" in conf:
            self.develop = conf['develop']
        
        
    # Get config.
    #
    def getConfig(self):
        blnVerify = (self.develop == False)

        request_headers = { "Content-Type" : "application/json",
                    "Accept":"application/json",
                    "Authorization" : "Bearer " + self.token }

        url = self.base_url + '/api/config/' + self.host_id

        response = requests.get(url,headers=request_headers,verify=blnVerify)
        json_data = json.loads(response.text)

        self.config_refresh = json_data['data']['updated_at']
        self.services = json_data['data']['service'];


    # Store data.
    #
    def storeData(self, serviceUuid, output):
        blnVerify = (self.develop == False)
        checked_at = time.time()
        
        payload = {
            "host_id": self.host_id,
            "services": [
                {"checked_at": checked_at, "service_id": serviceUuid, "data": output}
            ]
        }

        url = self.base_url + '/api/store/' + self.host_id
        request_headers = { "Content-Type" : "application/json",
                            "Accept" : "application/json",
                            "Authorization" : "Bearer " + self.token }
        
        response = requests.post(url, data=json.dumps(payload), headers=request_headers, verify=blnVerify)

        return response.json()


    # Check services.
    #
    def checkServices(self):
        intReturn = 0
        for service in self.services:
            service_id = service['id']

            if int(service["last_run"]) + int(service["interval"]) < time.time():
                cmd = (service['script']).split(':')
                
                obj = Script.factory(cmd[0])

                if (obj):
                    output = obj.run(service['warning'], service['critical'], cmd[1])
                    out = self.storeData(service_id, output)
                    intReturn = out['data']['updated_at']

                service["last_run"] = time.time()

        if (intReturn != 0 and intReturn > self.config_refresh):
            print("get new config")
            self.getConfig()
