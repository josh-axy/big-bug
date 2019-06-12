#%%
print("1111")
# import redis
import common
# import happybase
import crawler
import hbase_tools
import redis_tools
print("2222")

# rules=[
#     {
#         "selectors":[("#titleColumn > a",True)],
#         "reg":r"href=\"(.+?)\""
#     },
#     {
#         "selectors":[("h1",False)],
#     }
# ]

rules=[
    {
        "selectors":[(".hd > a",False)],
        "reg":r"href=\"(.+?)\""
    },
    {
        "selectors":[("h1",False)],
    }
]


job_core = crawler.CrawlJobCore("hahaha",rules)
urls=[
    # "https://www.imdb.com/chart/top?ref_=nv_mv_250_6"
    "https://movie.douban.com/top250"
]

try:
    hbase_tools.remove_job(job_core.name)
finally:
    pass
hbase_tools.save_job(job_core)
print("3333")
task_json = crawler.CrawlTaskJson(job_core.name,0,urls)
task_json_str = task_json.get_json()
redis_tools.CLOSE_SET.add(job_core.name)
redis_tools.CLOSE_SET.remove(job_core.name)
redis_tools.QUEUE.put(task_json_str)
print("4444")



import time 
time.sleep(1000)
#%%
print("OVER")
