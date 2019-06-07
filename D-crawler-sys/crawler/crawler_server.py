import common
import crawler
from collections.abc import Iterable

#tmp
import os
import random


class CrawlerServer:
    def __init__(self):
        self.task_queue = crawler.TaskQueue(maxsize=50)
        self.crawler = crawler.Crawler(
            self.task_queue.task_generator(),
            driver_cnt=3)
        # 用于去job重
        self.crawl_job_dict = dict()

    def __enter__(self):
        self.start()
        return self 
    
    def __exit__(self,exc_type, exc_value, traceback):
        self.close()

    def start(self):
        self.crawler.serve()

    def close(self):
        # 顺序别反了，否则发生死锁
        self.task_queue.close()
        self.crawler.close()
        # self.task_queue.close()

    def add_crawl_job(self,core:crawler.CrawlJobCore):
        assert isinstance(core.name,str) and core.name not in self.crawl_job_dict
        self.crawl_job_dict[core.name] = crawler.CrawlJob(core,self.save_fn)

    def add_urls(self,crawl_job_name:str,urls:Iterable):
        assert crawl_job_name in self.crawl_job_dict
        job = self.crawl_job_dict[crawl_job_name]
        self.task_queue.add_tasks(job,urls)

    def save_fn(self,
                crawl_job_core: crawler.CrawlJobCore,
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