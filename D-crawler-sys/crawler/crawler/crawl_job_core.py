__all__ = (
    "CrawlJobCore",
)

import re

class CrawlJobCore:
    def __init__(self, name: str, selectors: list, reg_pattern: str = None):
        self.name = name 
        self.selectors = selectors
        if reg_pattern is not None:
            self.reg_pattern = re.compile(reg_pattern)
        else:
            self.reg_pattern = None
