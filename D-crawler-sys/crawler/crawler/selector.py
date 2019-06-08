__all__ = (
    "Selector",
)

import common
import functools
import threading
from queue import Queue
from enum import Enum
import re
from collections.abc import Iterable
from selenium.common.exceptions import NoSuchElementException
# from selenium import webdriver


class Selector:
    '''
        用于寻找页面元素的选择器
        css_selector 是 CSS选择器字符串
        select_elements 是一个 bool 值，表示是否选取多个元素
        （但实际上，不管是取多个还是单个，最后统一返回列表，方便统一处理）
    '''

    def __init__(self,
                 css_selector: str,
                 select_elements: bool = False):
        assert css_selector is not None
        self.css_selector = css_selector
        self.select_elements = select_elements

    def select(self, target) -> list:
        '''
            target 是 select 作用的目标
            可以是 webdriver，也可以是 webelement
            （因为 selenium 提供了统一的 select_element_by_css_selector 接口）
        '''
        assert type(target) != str
        if isinstance(target, Iterable):
            result = []
            for ele in target:
                result.extend(self._select(ele))
            return result
        else:
            return self._select(target)

    def _select(self, target) -> list:
        # target:webdriver.firefox.webdriver.WebDriver
        if self.select_elements:
            return target.find_elements_by_css_selector(self.css_selector)
        else:
            try:
                ele = target.find_element_by_css_selector(self.css_selector)
                return [ele]
            except NoSuchElementException:
                return []

    @classmethod
    def make_selector_list(cls, selector_list_raw:list):
        '''
            由 CrawlTaskCore 的 selectors 信息生成 Selector 对象列表
            输入形式如下：
                [("#content",True),("h1",False)]
        '''
        assert not isinstance(selector_list_raw, str)
        selector_list = list()
        if selector_list_raw is not None:
            for ele in selector_list_raw:
                if isinstance(ele, str):
                    selector_list.append(cls(ele, False))
                elif isinstance(ele, Iterable):
                    if len(ele) >= 2:
                        selector_list.append(cls(ele[0], ele[1]))
                    elif len(ele) == 1:
                        selector_list.append(cls(ele[0], False))
                    else:
                        continue
        return selector_list
