import requests, json, time
import config

from prometheus_client import start_http_server
from prometheus_client import Gauge, Summary
from prometheus_client import REGISTRY

import time, random, os, platform
import prometheus_client

REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)


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


def GetNodeBalancers():
    url = config.loadbalance_url

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


def GetVolumes():
    url = config.volumes_url

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


def GetNetworkTransfer():
    url = config.network_quota_url

    resp = requests.get(url, headers=headers)
    #print(page, resp.status_code)
    data = json.loads(resp.text)
    
    return data

def GetLinodeTypes():
    url = config.instance_type_url

    resp = requests.get(url, headers=headers)
    #print(page, resp.status_code)
    data = json.loads(resp.text)

    instance_type = dict()
    for item in data['data']:
        type_id = item['id']
        instance_type[type_id] = float(item['price']['hourly'])
    
    return instance_type

    


if __name__ == '__main__':
    hostPort = config.hostPort
    hostAddr = config.hostAddr
    start_http_server(port=hostPort, addr=hostAddr)

    linodeInstanceTypeCount = Gauge("linode_instance_type_count", "Linode Instances Statistic", ["type"])
    linodeInstanceStatusCount = Gauge("linode_instance_status_count", "Linode Instances Statistic", ["status"])
    linodeNodebalancerCount = Gauge("linode_nodebalancer_count", "Linode NodeBalancer Statistic", [])
    linodeVolumesCount = Gauge("linode_volumes_count", "Linode Block Storage Statistic", ["status"])
    linodeVolumesSize = Gauge("linode_volumes_size", "Linode Block Storage Total GB", ["size"])
    linodeTrafficQuota = Gauge("linode_traffice_quota", "Linode Traffic Quota & Usage", ["type"])
    linodeEstimateCost = Gauge("linode_estimate_cost", "Linode Hourly Cost Estimated", ["type"])
    

    inteval = config.interval

    
    while(True):
        # linodeInstanceTypeCount.clear()
        # linodeInstanceStatusCount.clear()
        # linodeNodebalancerCount.clear()
        # linodeVolumesCount.clear()
        # linodeTrafficQuota.clear()


        try:
            instance_count = dict()
            instance_running = 0
            instance_notrunning = 0

            
            nodebalancer_count = 0
            
            volume_active = 0
            volume_inactive = 0
            volume_total = 0

            network_transfer_quota = 0
            network_transfer_usage = 0

            instances = GetInstances()
            for instance in instances:
                instance_type = instance['type']
                if instance_type in instance_count.keys():
                    instance_count[instance_type] += 1
                else:
                    instance_count[instance_type] = 1
                
                if instance['status'] == 'running':
                    instance_running += 1
                else:
                    instance_notrunning += 1

            for k,v in instance_count.items():
                linodeInstanceTypeCount.labels(k).set(v)

            nodebalancers = GetNodeBalancers()
            nodebalancer_count = len(nodebalancers)

            volumes = GetVolumes()
            for item in volumes:
                volume_total += int(item['size'])
                if item['linode_id'] is not None:
                    volume_active += 1
                else:
                    volume_inactive += 1
            
            network_transfer = GetNetworkTransfer()
            network_transfer_usage = network_transfer['used']
            network_transfer_quota = network_transfer['quota']
            

            # print(instance_count)
            # print(nodebalancers)
            # print(volumes)
            # print(network_transfer)



            linodeInstanceStatusCount.labels('running').set(instance_running)
            linodeInstanceStatusCount.labels('notrunning').set(instance_notrunning)

            linodeNodebalancerCount.set(nodebalancer_count)

            linodeVolumesCount.labels('attached').set(volume_active)
            linodeVolumesCount.labels('unattached').set(volume_inactive)
            linodeVolumesSize.labels('size').set(volume_total)

            linodeTrafficQuota.labels('used').set(network_transfer_usage)
            linodeTrafficQuota.labels('quota').set(network_transfer_quota)

            # Estimated Hourly Price for NodeBalance & Block Storage
            nodeBalanceTotal = nodebalancer_count * config.nodeBalancePrice
            volumeTotal = volume_total * config.storagePrice
            
            # Estimated Hourly Price for Linode Instances
            instance_types = GetLinodeTypes()
            # print(instance_types)
            instance_total = 0
            for k,v in instance_count.items():
                instance_total += v * instance_types[k]
                
            linodeEstimateCost.labels('nodebalance').set(nodeBalanceTotal)
            linodeEstimateCost.labels('blockstorage').set(volumeTotal)
            linodeEstimateCost.labels('instance').set(instance_total)

            print(instance_total, nodeBalanceTotal, volume_total)

            print("Refresh OK")
            time.sleep(inteval)
        
        except Exception as e:

            print("Error: ")
            print(e)

            time.sleep(5)




