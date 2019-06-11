import common
# import crawler
from collections.abc import Iterable, Callable

from .crawl_job import CrawlJob
from .crawl_job_core import CrawlJobCore
from .crawler import Crawler
from .task_queue import TaskQueue



class CrawlerService:
    '''
        爬虫服务
        封装了crawler模块里各种复杂操作，方便外部调用爬虫
    '''
    def __init__(self, save_fn: Callable):
        # 先判断 save_fn 的参数是否符合要求
        assert (
            set(common.inspect.get_params(save_fn)) ==
            set(("layer","crawl_job_core", "url", "result_list"))
        )
        self.task_queue = TaskQueue(maxsize=50)
        self.crawler = Crawler(
            self.task_queue.task_generator(),
            driver_cnt=3)
        # 用于保存结果的函数
        self.save_fn = save_fn

        # # 用于去job重
        # self.crawl_job_dict = dict()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def start(self):
        self.crawler.serve()

    def close(self):
        # 顺序别反了，否则发生死锁
        self.task_queue.close()
        self.crawler.close()

    def add_urls(self, crawl_job_core:CrawlJobCore,layer:int, urls: Iterable):
        job = CrawlJob(crawl_job_core,self.save_fn)
        self.task_queue.add_tasks(job,layer,urls)

    # def add_crawl_job(self, core: CrawlJobCore):
    #     assert isinstance(
    #         core.name, str) and core.name not in self.crawl_job_dict
    #     self.crawl_job_dict[core.name] = CrawlJob(core, self.save_fn)

    # def add_urls(self, crawl_job_name: str, urls: Iterable):
    #     assert crawl_job_name in self.crawl_job_dict
    #     job = self.crawl_job_dict[crawl_job_name]
    #     self.task_queue.add_tasks(job, urls)
