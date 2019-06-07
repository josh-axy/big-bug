__all__=(
    "Crawler",
)

from selenium import webdriver
import common
import functools
from concurrent.futures import ThreadPoolExecutor
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
        self.executor=ThreadPoolExecutor(max_workers=self.driver_cnt)
        self.end_flag = False
        self.end_func = lambda:self.end_flag
        self.__set_tasks(tasks)

        def serve_func():
            for d in self.drivers:
                self.executor.submit(
                    d.work,
                    self.tasks,
                    self.end_func
                )
        self.serve_thread = threading.Thread(target=serve_func)

    def serve(self):
        self.serve_thread.start()

    def close(self):
        self.end_flag = True 
        # shutdown，等待结束
        self.executor.shutdown(wait=True)
        self.serve_thread.join()

    def __set_tasks(self,tasks:common.LockedIterator):
        assert isinstance(tasks,Iterable)
        if not isinstance(tasks,common.LockedIterator):
            tasks = common.LockedIterator(tasks)
        self.tasks = tasks


class DriverWrapper:
    def __init__(self,web_driver_path:str):
        self.web_driver_path = web_driver_path
        self.driver = None
        
    def activate(self):
        # self.driver = webdriver.Firefox(executable_path=common.WEBDRIVER_PATH)
        self.driver = webdriver.Firefox(executable_path=self.web_driver_path)

    def close(self):
        if self.driver is not None:
            self.driver.close()

    def work(self,
            tasks: common.LockedIterator,
            end_func: Callable=lambda:True):
        while not end_func():
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