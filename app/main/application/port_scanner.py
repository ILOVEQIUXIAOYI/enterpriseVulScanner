"""
    Created by zltningx on 18-7-17.
"""

import nmap


def scanner(ip_list):
    try:
        nm_scanner = nmap.PortScanner()
    except Exception as e:
        print("run error: " + str(e))
        return 0
    hosts = ""
    for ip in ip_list:
        hosts += ip
    try:
        nm_scanner.scan(hosts=hosts, arguments='-A')
    except Exception as e:
        print("scanner error: " + str(e))
        return 0

    info = dict()
    for host in nm_scanner.all_hosts():
        info[host] = dict()
        for protocol in nm_scanner[host].all_protocols():
            info[host][protocol] = nm_scanner[host][protocol]
    return info


def run_time_scanner(ip_list):
    try:
        nm_scanner = nmap.PortScanner()
    except Exception as e:
        print("run error: " + str(e))
        return None
    hosts = ""
    for ip in ip_list:
        hosts += ip
        hosts += " "
    try:
        nm_scanner.scan(hosts=hosts, arguments='-A')
    except Exception as e:
        print("scanner error: " + str(e))
        return None
    info = dict()
    result = set()
    for host in nm_scanner.all_hosts():
        info[host] = dict()
        for protocol in nm_scanner[host].all_protocols():
            info[host] = list(nm_scanner[host][protocol].keys())
            for i in info[host]:
                result.add(i)
    return info, list(result)


if __name__ == '__main__':
    a = run_time_scanner(['e.sangfor.com.cn','www.baidu.com'])