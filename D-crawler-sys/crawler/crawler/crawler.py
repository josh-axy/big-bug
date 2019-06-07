__all__=(
    "Crawler",
)

from selenium import webdriver
import common
import functools
# from concurrent.futures import ThreadPoolExecutor
import threading
from collections.abc import Iterable,Callable

class DriverCnt:
    def __init__(self,name):
        self.name = name

    def __set__(self,instance,value):
        assert isinstance(value,int)
        value = value if value > 1 and value < 6 else 3
        instance.__dict__[self.name]=value

class Crawler:
    driver_cnt = DriverCnt("driver_cnt")
    def __init__(self,tasks,driver_cnt:int=3):
        self.driver_cnt = driver_cnt
        self.drivers = [DriverWrapper(common.WEBDRIVER_PATH) for i in range(driver_cnt)]
        self.end_flag = False
        self.__set_tasks(tasks)

        # 好像用 executor 不太好控制,比如 shutdown 时似乎没有阻塞？？（可能只是我用不习惯而已）
        # self.executor=ThreadPoolExecutor(max_workers=self.driver_cnt)
        self.threads = [
            threading.Thread(target=d.work,args=(self.tasks,))
            for d in self.drivers
        ]

    def serve(self):
        for t in self.threads:
            t.start()

    def close(self):
        for d in self.drivers:
            d.set_end()
        for t in self.threads:
            t.join()

    def __set_tasks(self,tasks:common.LockedIterator):
        assert isinstance(tasks,Iterable)
        if not isinstance(tasks,common.LockedIterator):
            tasks = common.LockedIterator(tasks)
        self.tasks = tasks


class DriverWrapper:
    def __init__(self,web_driver_path:str):
        self.web_driver_path = web_driver_path
        self.driver = None
        self.end_flag = False

    def set_end(self):
        self.end_flag = True
        
    def activate(self):
        # self.driver = webdriver.Firefox(executable_path=common.WEBDRIVER_PATH)
        self.driver = webdriver.Firefox(executable_path=self.web_driver_path)

    def close(self):
        if self.driver is not None:
            # # 似乎应该用quit 而不是close，否则结束时会报错
            self.driver.quit()
            self.driver.stop_client()
            # self.driver.close()

    def work(self,
            tasks: common.LockedIterator):
        while not self.end_flag:
            try:
                self.activate()
                for task in tasks:
                    task(self.driver)
            except Exception as e:
                common.print_exception(e)
                continue
            finally:
                self.close()

    def __del__(self):
        self.close()

# <class 'selenium.webdriver.firefox.webdriver.WebDriver'>