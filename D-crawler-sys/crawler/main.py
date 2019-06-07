import common
import crawler

from crawler_server import CrawlerServer

# with CrawlerServer() as C:
C =  CrawlerServer()
C.start()
job_core = crawler.CrawlJobCore("hahaha")
urls = [
    "http://tool.oschina.net/highlight",
    "https://baike.baidu.com/item/upx/4630968?fr=aladdin",
]
C.add_crawl_job(job_core)
C.add_urls(job_core.name,urls)

C.close()
print("OK")

print("OVER")