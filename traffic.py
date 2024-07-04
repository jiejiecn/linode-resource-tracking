import requests, json, time
import time, random, os, platform

import config



headers = {
    "Authorization": "Bearer " + config.linode_token,
    "Content-Type": "application/json"
}


def GetInstances():
    url = config.instances_url

    page = 1
    instances = []

    while True:

        param = {
            'page': page,
            'page_size': config.pagesize
        }

        resp = requests.get(url, 
                            headers=headers, 
                            params=param)
        #print(page, resp.status_code)
        data = json.loads(resp.text)

        page = data['page']
        pages = data['pages']

        for item in data['data']:
            instances.append(item)

        if page == pages:
            break
        else:
            page += 1
    
    return instances


def GetInstancTraffic(linodeid: int):
    url = config.instance_traffic

    url = url.replace('{{linodeid}}', str(linodeid))

    resp = requests.get(url, 
                        headers=headers)
    #print(page, resp.status_code)
    data = json.loads(resp.text)

    return data



linode_instances = GetInstances()
for item in linode_instances:
    linode_id = item['id']
    traffic = GetInstancTraffic(linode_id)

    print(item['label'], traffic)

    # record = database.InstanceTraffic()
    # record.linode_id = item['id']
    # record.linode_label = item['label']
    # record.instanceType = item['type']
    # record.dataCenter = item['region']
    # record.publicIp = item['ipv4'][0]
    # record.traffic_usage = traffic['used']
    # record.traffic_usage_GB = record.traffic_usage / 1024 / 1024 / 1024
    # record.traffic_quota = traffic['quota']
    # record.traffic_billable = traffic['billable']
    # record.traffic_billable_GB = record.traffic_billable / 1024 / 1024 / 1024

    

    # database.db.add(record)
    # database.db.commit()


