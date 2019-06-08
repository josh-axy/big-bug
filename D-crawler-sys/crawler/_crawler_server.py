import common
# import crawler
from crawler import *
from collections.abc import Iterable, Callable


# tmp
import os
import random

class CrawlerServer:
    '''
        用于测试
    '''
    def __init__(self):
        self.C = CrawlerService(self.save_fn)
        pass 

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def start(self):
        self.C.start()

    def close(self):
        self.C.close()

    def add_crawl_job(self, core: CrawlJobCore):
        self.C.add_crawl_job(core)

    def add_urls(self, crawl_job_name: str, urls: Iterable):
        self.C.add_urls(crawl_job_name, urls)

    def save_fn(self,
                crawl_job_core: CrawlJobCore,
                url: str,
                result_list: list):
        d = "tmptmptmp"
        if not os.path.exists(d):
            os.mkdir(d)
        core_name = crawl_job_core.name
        path=os.path.join(d,core_name + url.split("/")[2])+str(random.randint(0,10000))+".txt"
        with open(path,"w") as fw:
            fw.write(str(result_list))
        pass