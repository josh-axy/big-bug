__all__ = (
    "CrawlJobCore",
)

import re

class CrawlJobCore:
    def __init__(self, name: str, extractors: list, reg_pattern: str):
        self.name = name 
        self.extractors = extractors
        self.reg_pattern = re.compile(reg_pattern)
