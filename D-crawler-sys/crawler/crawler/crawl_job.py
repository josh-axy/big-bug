__all__ = (
    "CrawlJob",
)

import functools
from collections.abc import Callable
from .crawl_job_core import CrawlJobCore

from selenium import webdriver


class CrawlJob:
    def __init__(self, crawl_job_core: CrawlJobCore, save_fn: Callable):
        '''
            save_fn 应该有以下几个参数:
                crawl_job_core = self.core,
                url = url,
                result_list = result_list
        '''
        self.core = crawl_job_core
        self.save_fn = save_fn

    def work(self, driver, url):
        driver:webdriver.firefox.webdriver.WebDriver
        driver.get(url)
        result_list=[]
        if len(self.core.selectors)<=0:
            content=driver.page_source
            if self.core.reg_pattern is not None:
                result_list.extend(self.core.reg_pattern.findall(content))
            else:
                result_list=[content]
        else:
            target = driver
            for selector in self.core.selectors:
                target = selector.select(target)
            for ele in target:
                content = ele.get_attribute("innerHTML")
                if self.core.reg_pattern is not None:
                    result_list.extend(self.core.reg_pattern.findall(content))
        # 调用 save 函数
        self.save_fn(crawl_job_core=self.core,
                     url=url,
                     result_list=result_list)

    def tasks_gen(self, urls):
        for url in urls:
            task = functools.partial(self.work, url=url)
            yield task
