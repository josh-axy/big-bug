__all__ = (
    "CrawlTaskCore",
)

import common
import functools
import threading
from queue import Queue
from enum import Enum
import re

from selenium import webdriver

class ExtractorType(Enum):
    TAG = 0,
    ID = 1,
    CLASS = 2,
    KEY_VALUE = 3,

x:webdriver.firefox.webdriver.WebDriver

class Extractor:
    extractor_func = {

    }
    def __init__(self,extractor_type:ExtractorType,v):
        assert extractor_type in ExtractorType
        self._type = extractor_type

    def extract(self,target):
        # if self._type
        pass


class CrawlTaskCore:
    def __init__(self,name:str,extractor:list,reg_pattern:str):
        pass

    def work(self, driver, url):
        pass
