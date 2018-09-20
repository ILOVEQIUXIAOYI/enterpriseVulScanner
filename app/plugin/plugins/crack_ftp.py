"""
    Created by zltningx on 18-4-30.
"""

from concurrent.futures import ThreadPoolExecutor

import socket
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
        info = plugin_info()
        info['ip'] = ip
        info['login_type'] = "user password required"
        info['description'] = "可使用弱账户密码登录ftp服务器"
        return info


def loginanonymously(ip, user_list):
    try:
        ftp = ftplib.FTP(ip)
        ftp.login()
    except ftplib.all_errors:
        print("Login as Anonymously False! {}".format(ip))
        try:
            with ThreadPoolExecutor(3) as Executor:
                with open("lib/dict/ftp_dict",'r') as passwdfile:
                    for user in user_list:
                        for passwd in passwdfile:
                            passwd = passwd.strip('\n')
                            try:
                                Executor.submit(login, ip, user, passwd)
                            except Exception as e:
                                print(e)
        except ftplib.all_errors:
            pass
    else:
        print("Login success!--------------->  {}".format(ip))
        info = plugin_info()
        info['ip'] = ip
        info['login_type'] = "Anonymously"
        info['description'] = "可使用匿名方式登录ftp服务器"
        return info


def conn(ip, user_list):
    try:
        serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        check = serv.connect_ex((ip, 21))
        if check == 0:
            loginanonymously(ip)
        else:
            print("[+]{} No Found FTP".format(ip))
        serv.close()
    except Exception as e:
        print(e)
        pass


def run(ip_list, port_list, timeout=10):
    user_list = ['ftp', 'www', 'admin', 'root', 'db', 'wwwroot', 'data', 'web']
    socket.setdefaulttimeout(2.5)
    with ThreadPoolExecutor(10) as executor:
        for ip in ip_list:
            try:
                executor.submit(conn, ip, user_list)
            except Exception as e:
                pass


if __name__ == '__main__':
    pass