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

# from selenium import webdriver


class Selector:
    def __init__(self,
                 css_selector:str = None,
                 select_elements: bool = False):
        self.css_selector = css_selector
        self.select_elements = select_elements

    def select(self, target)->list:
        assert type(target)!=str
        if isinstance(target,Iterable):
            result = []
            for ele in target:
                result.extend(self._select(ele))
            return result
        else:
            return self._select(target)

    def _select(self, target)->list:
        if self.css_selector is None:
            return [target]
        # target:webdriver.firefox.webdriver.WebDriver
        if self.select_elements:
            return target.find_elements_by_css_selector(self.css_selector)
        else:
            ele = target.find_element_by_css_selector(self.css_selector)
            return [] if ele is None else [ele]


