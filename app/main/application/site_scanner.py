import requests
import time

from sys import stdout
from concurrent.futures import ThreadPoolExecutor
from urllib import parse


headers = {
    "User-Agent": "User-Agent:Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en\
    -us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50"
}


class DirectorScanner(object):
    def __init__(self, url):
        if not 'http' in url:
            url = 'http://' + url
        self.url = url
        self.lib = set()

    def run(self, threadNumber):
        with open("lib/dict/director_scanner.txt") as f:
            with ThreadPoolExecutor(threadNumber) as executor:
                for line in f:
                    executor.submit(self.crack, line)
        return self.lib

    def crack(self, line):
        url = parse.urljoin(self.url, line)
        res = requests.get(url, headers=headers)
        if res.status_code >= 200 and res.status_code <= 399 and not "404" in res.content:
            self.lib.add((url, res.status_code))
            stdout.write("test: " +line.strip() + "--" + str(res.status_code))
            stdout.flush()

    def _to_html(self):
        with open("lib/tmp/"+self.url+".html", 'w') as f:
            f.write("<html><h1>"+self.url+" - 目录爆破工具 By zltningx </h1>\n")
            for item in self.lib:
                f.write("<li>{} : {}</li>\n".format(item[0], item[1]))
            f.write("</html>")


if __name__ == '__main__':
    director_scanner = DirectorScanner('http://www.baidu.com')
    a = director_scanner.run(100)
    director_scanner._to_html()
