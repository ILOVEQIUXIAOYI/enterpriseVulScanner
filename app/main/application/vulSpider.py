from urllib import parse
from scrapy.selector import Selector
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from time import sleep


import requests


class vulSpider():
    def __init__(self, url):
        if not 'http' in url:
            url = 'http://' + url
        self.url = url
        self.visited = set()
        self.queue = Queue()
        global count
        count = 0

    def run(self):
        self.parse(self.url)
        with ThreadPoolExecutor(10) as executor:
            while True:
                url = self.queue.get()
                if url not in self.visited:
                    executor.submit(self.parse, url)
                if self.queue.empty():
                    sleep(5)
                    if self.queue.empty():
                        print('执行结束断开链接')
                        break

    def parse(self, url):
        global count
        count += 1
        self.visited.add(url)
        headers = {
            "User-Agent": "User-Agent:Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en\
            -us)AppleWebKit/534`.50(KHTML,likeGecko)Version/5.1Safari/534.50"
        }
        res = requests.get(self.url, headers=headers)
        selector = Selector(text=res.text)
        urls = selector.css("*::attr(href)").extract()
        for url in urls:
            url = parse.urljoin(self.url, url)
            if self.url in url:
                self.queue.put(url)

    def store(self, url, wight):
        pass