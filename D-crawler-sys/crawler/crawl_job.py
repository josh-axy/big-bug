__all__ = (
    "CrawlJob",
)

import functools
from crawl_task_core import CrawlTaskCore

class CrawlJob:
    def __init__(self, crawl_task_core: CrawlTaskCore):
        self.core = crawl_task_core

    def tasks_gen(self, urls):
        for url in urls:
            task = functools.partial(self.core.work, url=url)
            yield task