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
        yield
        self.C.close()

    def add_crawl_job(self, core: CrawlJobCore):
        self.C.add_crawl_job(core)

    def add_urls(self, crawl_job_name: str, urls: Iterable):
        self.C.add_urls(crawl_job_name, urls)

    def save_fn(self,
                crawl_job_core: CrawlJobCore,
                url: str,
                result_list: list):
        '''
            该函数用于保存爬取的数据
        '''
        '''
            TODO 现在这里只是临时的函数
        '''
        d = "tmptmptmp"
        if not os.path.exists(d):
            os.mkdir(d)
        core_name = crawl_job_core.name
        path=os.path.join(d,core_name + url.split("/")[2])+str(random.randint(0,10000))+".txt"
        with open(path,"w") as fw:
            fw.write(str(result_list))
        pass

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
        @self.controller("POST","/hello")
        async def hello(request:web.Request):
            return web.Response(body="hello")