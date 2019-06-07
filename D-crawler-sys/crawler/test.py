# import common
# import crawler

# if __name__=="__main__":
#     pass


#%%
import common
from selenium import webdriver
# import bs4

driver = webdriver.Firefox(executable_path=common.WEBDRIVER_PATH)
driver.get("https://www.baidu.com/")
# print(driver.page_source)
# source = 

#%%
target = driver.find_element_by_id("lg")
ans = target.get_attribute("innerHTML")
print(ans)

# selenium.common.exceptions.NoSuchElementException