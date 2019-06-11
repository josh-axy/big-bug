__all__ = (
    "CrawlJob",
)

import functools
from collections.abc import Callable
from .crawl_job_core import CrawlJobCore
from .selector import Selector

# from selenium import webdriver
import common


class CrawlJob:
    '''
        根据 CrawlJobCore 和 save_fn 构造爬虫任务
        CrawlJobCore 的描述见其源码注释
        save_fn 是一个函数（或者可调用对象），用于处理爬取数据的存储问题
    '''

    def __init__(self, crawl_job_core: CrawlJobCore, save_fn: Callable):
        '''
            save_fn 应该有以下几个参数:
                crawl_job_core = self.core,
                url = url,
                result_list = result_list
        '''
        # 先判断 save_fn 的参数是否符合要求
        assert (
            set(common.inspect.get_params(save_fn)) ==
            set(("layer", "crawl_job_core", "url", "result_list"))
        )
        self.core = crawl_job_core
        self.save_fn = save_fn
        self.selectors = [
            Selector.make_selector_list(rule["selectors"])
            for rule in self.core.rules
        ]

    # TODO 还没有去重功能，应该可以用布隆过滤器
    def work(self, driver, url, layer: int):
        '''
            work 方法是爬虫运行部分
            是实际上的 crawl_task
            利用 selenium 的 webdriver 爬取数据

            driver : selenium 的 WebDriver，用于控制浏览器
            url : 是要爬去的 url
            layer : 是当前要爬去的层级
        '''
        # 首先检查 url 合法性和 layer 合法性
        assert common.urltools.check_url(url)
        assert isinstance(layer,int) and layer >= 0 and layer < self.core.layer_cnt()
        selectors = self.selectors[layer]
        reg = self.core.rules[layer]["reg"]
        # 打印开始信息
        common.print_info(
            "[Task start: layer {}] --> CrawlJob({}): {}".format(layer, self.core.name, url))
        # driver:webdriver.firefox.webdriver.WebDriver
        driver.get(url)
        result_list = []
        if len(selectors) <= 0:
            content = driver.page_source
            if reg is not None:
                result_list.extend(reg.findall(content))
            else:
                result_list = [content]
        else:
            target = driver
            selector: Selector
            for selector in selectors:
                target = selector.select(target)
            for ele in target:
                # content = ele.get_attribute("innerHTML")
                content = ele.get_attribute("outerHTML")
                if reg is not None:
                    result_list.extend(reg.findall(content))
                else:
                    result_list.append(content)
        # 如果当前层级不是最后一个，需要保证结果为合法的url
        if layer != self.core.layer_cnt()-1:
            for url in result_list:
                assert common.urltools.check_url(url)
        # 调用 save 函数
        self.save_fn(
            layer=layer,
            crawl_job_core=self.core,
            url=url,
            result_list=result_list)
        # 打印结束信息
        common.print_info(
            "[Task done: layer {}] ==> CrawlJob({}): {}".format(layer, self.core.name, url))

    def tasks_gen(self, layer: int, urls: list):
        '''
            接收 url 列表
            对每个 url 生成 crawl_task 偏函数
        '''
        for url in urls:
            task = functools.partial(self.work, url=url, layer=layer)
            yield task
