__all__ = (
    "TaskQueue",
)

import common
from queue import Queue
from collections.abc import Iterable
from .crawl_job import CrawlJob


class TaskQueue:
    '''
        task 队列（Queue 线程安全）
        用于爬虫线程与其他线程的通信
    '''

    def __init__(self, maxsize=50):
        self.queue = Queue(maxsize=maxsize)
        self.closed = False

    def add_tasks(self, crawl_job: CrawlJob, layer: int, urls: Iterable):
        '''
            根据 CrawlJob 和 url 列表为爬虫生成 task，并加入队列
        '''
        for task in crawl_job.tasks_gen(layer,urls):
            if not self.closed:
                self.queue.put(task)

    # 先将其转换为线程安全的生成器
    @common.thread_safe_generator
    def task_generator(self):
        '''
            构造一个线程安全的生成器
            用于从队列里取出 task 提供给爬虫
            （提供形式为 for 循环调用生成器）
        '''
        while not self.closed:
            task = self.queue.get()
            # 注意，需要 task_done 才能使 queue.join 正常运作
            self.queue.task_done()
            if task is None:
                break
            yield task
        return

    def close(self):
        if not self.closed:
            # 先放一个 None 表示终止信息
            self.queue.put(None)
            self.queue.join()
            self.closed = True

    def __del__(self):
        if not self.closed:
            self.close()
