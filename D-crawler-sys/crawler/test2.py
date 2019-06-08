import common
import crawler

from _crawler_server import CrawlerServer

with CrawlerServer() as C:
    job_core = crawler.CrawlJobCore("hahaha",[("#content",True),("h1",False)],r"<span class=\"year\">(.+?)</span>")

    urls = [
        "https://movie.douban.com/subject/27053945/?tag=%E7%83%AD%E9%97%A8&from=gaia",
        "https://movie.douban.com/subject/27060077/?tag=热门&from=gaia_video",
        "https://movie.douban.com/subject/26266893/?tag=%E7%83%AD%E9%97%A8&from=gaia_video",
        "https://movie.douban.com/subject/30334073/?tag=%E7%83%AD%E9%97%A8&from=gaia_video",
        "https://movie.douban.com/subject/30403333/?tag=%E7%83%AD%E9%97%A8&from=gaia",
        "https://movie.douban.com/subject/30428225/?tag=%E7%83%AD%E9%97%A8&from=gaia",
    ]
    C.add_crawl_job(job_core)
    C.add_urls(job_core.name,urls)

print("OK")

print("OVER")