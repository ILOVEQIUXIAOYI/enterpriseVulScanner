"""hahaha
    Created by zltningx on 18-4-30.
"""

from time import sleep
from concurrent.futures import ThreadPoolExecutor

import socket
import os
import sys
import ftplib

recommend_port = [
    '21',
]


def plugin_info():
    plugin_info = {
        "name": "ftp弱口令",
        "author": "zltningx",
        "level": "High",
        "type": "WeekPassword",
        "url": "",
    }
    return plugin_info


def login(ip,user,passwd):
    try:
        ftp = ftplib.FTP(ip)
        ftp.login(user,passwd)
    except ftplib.all_errors:
        pass
    else:
        print("Login success!--------------> {}".format(ip))
        with open(os.path.abspath('.')+'/ftpaccount.txt','a+') as f:
            f.write(ip+'#'+user+'#'+passwd+'\n')
        ftp.quit()


def loginanonymously(ip):
    try:
        ftp = ftplib.FTP(ip)
        ftp.login()
    except ftplib.all_errors:
        print("Login as Anonymously False! {}".format(ip))
        try:
            with ThreadPoolExecutor(3) as Executor:
                with open(sys.argv[1],'r') as userfile:
                    with open(sys.argv[2],'r') as passwdfile:
                        for user in userfile:
                            user = user.strip('\n')
                            for passwd in passwdfile:
                                passwd = passwd.strip('\n')
                                try:
                                    Executor.submit(login,ip,user,passwd)
                                except Exception as e:
                                    print(e)
                                    pass
        except ftplib.all_errors:
            pass
    else:
        print("Login success!--------------->  {}".format(ip))
        with open(os.path.abspath('.')+'/ftpanonymously.txt','a+') as f:
            f.write(ip+'\n')
        ftp.quit()


def conn(ip, port):
    try:
        serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        check = serv.connect_ex((ip, port))
        if check == 0:
            loginanonymously(ip)
            with open(os.path.abspath('.')+'/open21.txt','a+') as f:
                f.write(ip+'\r\n')
        else:
            print("[+]{} No Found FTP Port on {}".format(ip, port))
        serv.close()
    except Exception as e:
        print(e)
        pass


def run(ip_list, port_list, timeout=10):
    user_list = ['ftp', 'www', 'admin', 'root', 'db', 'wwwroot', 'data', 'web']
    socket.setdefaulttimeout(2.5)
    with ThreadPoolExecutor(10) as executor:
        for ip in ip_list:
            for port in port_list:
                try:
                    executor.submit(conn, ip)
                except Exception as e:
                    pass