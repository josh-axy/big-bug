import common

# import crawler
from crawler import *
from collections.abc import Iterable, Callable
from contextlib import contextmanager
from collections import namedtuple
import os
import random
import asyncio
from aiohttp import web
import json
import threading
# 取名 QUEUE,DB 是为了应付换数据库的情况（名字对应不上就很尴尬）
from redis_tools import QUEUE
from redis_tools import CLOSE_SET
import hbase_tools as DB

import time


class CrawlJobException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class CrawlerServer:
    '''
        提供爬虫服务
        （访问数据库，调用爬虫）
    '''

    def __init__(self):
        self.C = CrawlerService(self.save_fn)
        self.ip = common.args.ip
        self.port = common.args.port

        self.RouteParam = namedtuple(
            "RouteParam", ["method", "path", "handler"])
        self.route_param_list = []

        self.end_flag = False
        self.timeout = 20  # redis 队列 pop 等待 超时时间
        self.thread_task_fetcher = threading.Thread(
            target=self.run_task_fetcher)

        # crawl_job 的 LRU 缓存
        self.job_lru_cache = common.lru_cache.LRUCache(capacity=30)
        pass

    def start(self):
        with self.run_crawler():
            # 这里利用了 run_forever 阻塞了主线程
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.init_app(loop))
            loop.run_forever()

    @contextmanager
    def run_crawler(self):
        '''
            CrawlerService 的上下文管理器
            优势是出错后能跳到__exit__部分把关闭工作给做了
        '''
        self.C.start()
        self.thread_task_fetcher.start()
        yield
        self.end_flag = True  # 设置终结
        self.thread_task_fetcher.join()
        self.C.close()

    def run_task_fetcher(self):
        '''
            从 redis 中获取 任务
        '''
        while not self.end_flag:
            try:
                obj_tuple = QUEUE.get_wait(timeout=self.timeout)
                # print(obj)
                if obj_tuple is None:
                    # 取出为空，说明超时了
                    continue
                _, content = obj_tuple
                task_info = CrawlTaskJson.from_json_str(content)
                # 如果该任务在 close_set 里，说明它被手动关闭了
                if CLOSE_SET.is_member(task_info.job_name):
                    common.print_info("this crawl_job has been closed: {}".format(task_info.job_name))
                    continue 
                # 判断是否为合法url
                for url in task_info.urls:
                    assert common.urltools.check_url(url)
                # 阻塞一段时间，防止其他节点抢不到
                time.sleep(0.5)
                self.add_urls(
                    task_info.job_name,
                    task_info.layer,
                    task_info.urls
                )
            except Exception as e:
                common.print_exception(e)

    # def add_crawl_job(self, core: CrawlJobCore):
    #     self.C.add_crawl_job(core)

    def add_urls(self, crawl_job_name: str, layer: int, urls: Iterable):
        # 如果该任务在 close_set 里，说明它被手动关闭了
        if CLOSE_SET.is_member(crawl_job_name):
            common.print_info("this crawl_job has been closed: {}".format(crawl_job_name))
            return
        # self.C.add_urls(crawl_job_name, urls)
        job_core: CrawlJobCore
        job_core = self.job_lru_cache.get(crawl_job_name)
        if job_core is None:
            # 如果缓存中没有，从数据库获取
            job_core = DB.get_job_rule(crawl_job_name)
            if job_core is None:
                raise CrawlJobException(
                    "No such crawl job: {}".format(crawl_job_name))
            self.job_lru_cache.put(crawl_job_name,job_core)
        self.C.add_urls(job_core, layer, urls)

    def save_fn(self,
                layer: int,
                crawl_job_core: CrawlJobCore,
                url: str,
                result_list: list):
        '''
            该函数用于保存爬取的数据
        '''
        # 如果该任务在 close_set 里，说明它被手动关闭了
        # assert not CLOSE_SET.is_member(crawl_job_core.name)
        if CLOSE_SET.is_member(crawl_job_core.name):
            common.print_info("this crawl_job has been closed: {}".format(crawl_job_core.name))
            return 
        assert layer >= 0 and layer < crawl_job_core.layer_cnt()
        # 如果到了最后一层，应该存数据到外村数据库
        if layer == crawl_job_core.layer_cnt()-1:
            flag = DB.save_results(crawl_job_core, url, result_list)
            if not flag:
                common.print_info("failed to save results")
        # 否则认为是中间结果，加入队列
        # 中间结果只支持 url
        else:
            # 首先判断是否结果为url
            for url in result_list:
                assert common.urltools.check_url(url)
            # 加入队列
            _job_name =crawl_job_core.name
            _layer = layer+1
            for url in result_list:
                # 这里的 task 我设置成 url 仅一个，只是为了方便
                task = CrawlTaskJson(_job_name,_layer,[url])
                task_json = task.get_json()
                # 加入队列
                QUEUE.put(task_json)


    def run_app(self):
        # loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.init_app(loop))
        loop.run_forever()
        pass

    async def init_app(self, loop):
        app = web.Application(loop=loop)
        self._build_controllers()
        # self._init_add_static(app)
        self._init_add_route(app)
        srv = await loop.create_server(app.make_handler(), self.ip, self.port)
        print('Py server started at {}:{}...'.format(self.ip, self.port))
        return srv

    '''
    以下为初始化函数
    '''

    def _init_add_route(self, app):
        '''
        为webapp设置路由
        '''
        for ele in self.route_param_list:
            app.router.add_route(ele.method, ele.path, ele.handler)

    def controller(self, method, path):
        '''
        controller装饰器，模仿springboot
        '''
        def wrapper(func):
            self.route_param_list.append(self.RouteParam(
                method=method, path=path, handler=func))
            return func
        return wrapper

    def _build_controllers(self):
        '''
        controllers
        '''
        @self.controller("POST", "/hello")
        async def hello(request: web.Request):
            return web.Response(body="hello")
