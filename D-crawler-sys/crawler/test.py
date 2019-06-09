#%%
import crawler
from crawler import CrawlJobCore

# core = crawler.CrawlJobCore("hahaha",[("#content",True),("h1",False)],r"<span class=\"year\">(.+?)</span>")
core = crawler.CrawlJobCore("hahaha")
st = core.dumps()
core = CrawlJobCore.loads(st)
print(core)
#%%
print("OVER")