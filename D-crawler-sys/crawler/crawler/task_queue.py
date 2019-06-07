__all__ = (
    "TaskQueue",
)

from queue import Queue
from .crawl_job import CrawlJob

class TaskQueue:
    def __init__(self, maxsize=50):
        self.queue = Queue(maxsize=maxsize)

    def add_tasks(self, crawl_job: CrawlJob, urls):
        for task in crawl_job.tasks_gen(urls):
            self.queue.put(task)

    def get_task(self):
        while True:
            task = self.queue.get()
            if task is None:
                break

    def close(self):
        self.queue.put(None)

    def __del__(self):
        pass # ??????