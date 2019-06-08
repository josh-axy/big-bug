# import common
# import crawler

# if __name__=="__main__":
#     pass


# #%%
# import common
# from selenium import webdriver
# # import bs4

# driver = webdriver.Firefox(executable_path=common.WEBDRIVER_PATH)
# driver.get("https://movie.douban.com/subject/27053945/?tag=%E7%83%AD%E9%97%A8&from=gaia")
# # print(driver.page_source)
# # source = 

# #%%
# # target = driver.find_element_by_id("content")
# target = driver.find_element_by_css_selector("#content")
# ans = target.get_attribute("innerHTML")
# print(ans)
# driver.close()

# selenium.common.exceptions.NoSuchElementException

#%%
from crawler_server import CrawlerServer
import crawler

with CrawlerServer() as C:
    job_core = crawler.CrawlJobCore("hahaha",[crawler.Selector("#content",True)])

    urls = [
        "https://movie.douban.com/subject/27053945/?tag=%E7%83%AD%E9%97%A8&from=gaia",
    ]
    C.add_crawl_job(job_core)
    C.add_urls(job_core.name,urls)

#%%
print("OVER")