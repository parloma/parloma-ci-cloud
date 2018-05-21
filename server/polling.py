#!/usr/bin/env python
# license removed for brevity

import requests
import uuid
import time
import ifcfg as ic
import os
from server.config import configs
import json


endpoint = "http://test.hotblackrobotics.com/api/robots/1.0"
config = configs[os.environ.get('CONFIG_SERVER') or 'default']
fdb = config.DB_PATH

poll_time = int(os.environ.get("POLL_TIME") or 1)
print(poll_time)

def main():
    try:
        with open(fdb,"r") as f:
            db = json.load(f)    
    except IOError:
        db = {}
        
    if 'rid' not in db.keys():
        db = {**db, 'rid':  str(uuid.uuid4())}
        print("generated db:" , db)
        with open(fdb,"w") as f:
            json.dump(db, f)

    print("passed db:", db)

    res = requests.post(endpoint+'/auth', json={"rid":db.get("rid")})
    token = res.json()["access_token"]
    headers={"Authorization": "Bearer {}".format(token)}
    print(headers)

    while True:
        ips = get_ips()
        res = requests.post(endpoint+'/poll', json={"ips": ips}, headers=headers)
        print(ips, res.json())
        time.sleep(poll_time)

def get_ips():
    ips_list=[]
    for interface, value in ic.interfaces().items():
        if interface not in ['lo', 'docker0']:
            if value['inet'] is not None:
                dic = {'interface':interface, 'ip':value['inet']}
                ips_list.append(dic)
    return ips_list

if __name__ == "__main__":
    main()