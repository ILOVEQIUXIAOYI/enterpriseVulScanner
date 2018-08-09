"""
    Created by zltningx on 18-4-29.
"""

from iptools import IpRange
import pickle

from .models import Plugin


def dump(obj):
    return pickle.dumps(obj)


def load(obj):
    return pickle.loads(obj)


def ip_recognize(ip):
    if ' ' in ip:
        ip = ip.strip('\r\n').split()
        ip_list = IpRange(ip[0], ip[1])
        return ip_list
    elif ',' in ip:
        ip = ip.split(',')
        return ip
    elif '/' in ip:
        ip_list = IpRange(ip)
        return ip_list
    else:
        return [ip]


def gen_recommend(port_list):
    plugins = Plugin.query.all()
    recommend_plugins = list()
    for port in port_list:
        for plugin in plugins:
            if port in plugin.get_recommend_port():
                recommend_plugins.append(plugin)
    return recommend_plugins