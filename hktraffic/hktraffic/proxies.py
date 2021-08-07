from hktraffic.settings import proxy_username, proxy_password

import os
import random
import requests


def getallproxies(force_update=False, resetcooldowns=False) -> list:
    
    if 'proxy_ips' in os.environ.keys() and force_update == False:
        if resetcooldowns:
            ips = os.environ['proxy_ips'].split(',')
            for i, proxy in enumerate(ips):
                ip = proxy.split(':')[0]
                port = proxy.split(':')[1]
                ips[i] = ':'.join([ip, port, '0'])
            os.environ['proxy_ips'] = ','.join(ips)
        else:
            ips = os.environ['proxy_ips'].split(',')
    else:
        url = f'https://blazingseollc.com/proxy/dashboard/api/export/4/all/{proxy_username}/{proxy_password}/list.csv'
        response = requests.get(url)

        ips = [':'.join(ip_port.split(':')[0:2])+':0' for ip_port in str(response.content)[2:].split('\\n')]
        random.shuffle(ips)
        os.environ['proxy_ips'] = ','.join(ips)
        os.environ['proxy_rotation'] = '0'
    
    # shuffle the list of ips any time we start a new iteration through them all
    if os.environ['proxy_rotation'] == '0':
        random.shuffle(ips)
        os.environ['proxy_ips'] = ','.join(ips)
        
    # returns list of ip:port
    return ips


def getproxy() -> dict:
    
    # proxies automatically cycle through using rotation (os.environ['proxy_rotation'])
    ips = getallproxies()

    rotation = int(os.environ['proxy_rotation'])
       
    ip = ips[rotation].split(':')[0]
    port = ips[rotation].split(':')[1]
    cooldown = int(ips[rotation].split(':')[2])
    # if proxy server is marked for cooldown, reduce the wait by the number of proxies that have run since last check
    if cooldown:
        cooldown -= len(ips)
        if cooldown < 0:
            cooldown = '0'
        ips[rotation] = ':'.join([ip, port, str(cooldown)])
        os.environ['proxy_ips'] = ','.join(ips)
    rotation += 1
    # if we reach the end of the list we go back to the first proxy
    if rotation == len(ips):
        rotation = 0
    os.environ['proxy_rotation'] = str(rotation)
    # if we're on cooldown, cycle to next one
    if cooldown:
        proxy = getproxy()
        return proxy

    http = f'http://{proxy_username}:{proxy_password}@{ip}:{port}'
    https = f'http://{proxy_username}:{proxy_password}@{ip}:{port}'
    ftp = f'ftp://{proxy_username}:{proxy_password}@{ip}:{port}'
    proxy = {'http': http,
             'https': https,
             'ftp': ftp}
    return proxy


def setcooldown(proxy, cooldown):
    
    ips = getallproxies()
    
    proxy_ip = proxy['http'].split('@')[1].split(':')[0]
    
    for i, ip in enumerate(ips):
        if proxy_ip == ip.split(':')[0]:
            port = ip.split(':')[1]
            ips[i] = ':'.join([proxy_ip, port, str(cooldown)])
            os.environ['proxy_ips'] = ','.join(ips)
            print(f' Proxy {proxy_ip} cooldown set to {cooldown}')
            return

    print(f'IP address {proxy_ip} not found') 
