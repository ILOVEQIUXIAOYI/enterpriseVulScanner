"""hahaha
    Created by zltningx on 18-4-30.
"""

from time import sleep
import os

recommend_port = [
    '22',
    '80'
]


def plugin_info():
    plugin_info = {
        "name": "ftp弱口令",
        "author": "",
        "level": "High",
        "type": "WeekPassword",
        "url": "",
    }
    return plugin_info


def run(ip_list, port_list, timeout=10):
    if not port_list:
        port_list = recommend_port
    sleep(1)
    print('test')
    return {
        'name': 'ftp弱口令',
        'level': 'high',
        'result': 1,
    }


