__all__ = (
    "CrawlJob",
)

import functools
from .crawl_job_core import CrawlJobCore


class CrawlJob:
    def __init__(self, crawl_job_core: CrawlJobCore):
        self.core = crawl_job_core

    def tasks_gen(self, urls):
        for url in urls:
            task = functools.partial(self.core.work, url=url)
            yield task