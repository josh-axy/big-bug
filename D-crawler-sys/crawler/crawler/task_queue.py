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

    def task_generator(self):
        while True:
            task = self.queue.get()
            # 注意，需要 task_done 才能使 queue.join 正常运作
            self.queue.task_done()
            if task is None:
                break
            yield task
        return

    def close(self):
        self.queue.put(None)
        self.queue.join()

    def __del__(self):
        pass # ??????