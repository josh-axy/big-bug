__all__ = (
    "CrawlJobCore",
)

import re

class CrawlJobCore:
    def __init__(self, name: str, selectors: list = None, reg_pattern: str = None):
        self.name = name 
        
        if selectors is not None:
            self.selectors = selectors
        else:
            self.selectors = []

        if reg_pattern is not None:
            self.reg_pattern = re.compile(reg_pattern)
        else:
            self.reg_pattern = None
