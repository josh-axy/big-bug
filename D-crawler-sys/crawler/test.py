#%%
print("1111")
# import redis
import common
# import happybase
import crawler
import hbase_tools
import redis_tools
print("2222")
# hbase_conn = happybase.Connection("localhost",port=9090,table_prefix="test",table_prefix_separator="_")
# # hbase_conn = happybase.Connection("localhost",port=9000,protocol='compact',transport='framed')
# print(hbase_conn.tables())
# # table = hbase_conn.compact_table()
# t = "tmp"
# if t not in hbase_conn.tables():
#     hbase_conn.create_table(t,families={"family":dict(max_versions=1),})
# table = hbase_conn.table(t)

# # table.put(b"tmp",{b"t1:test1":b"ttt",b"t2:test2":b"ttt"})
# table.put(b'row-key', {b'family:qual1': b'value1',
#                        b'family:qual2': b'value2'})

job_core = crawler.CrawlJobCore("hahaha",[("#content",True),("h1",False)],r"<span class=\"year\">(.+?)</span>")
urls=[
    "https://movie.douban.com/subject/27053945/?tag=%E7%83%AD%E9%97%A8&from=gaia",
    "https://movie.douban.com/subject/27060077/?tag=热门&from=gaia_video",
]
hbase_tools.remove_job(job_core.name)
hbase_tools.save_job(job_core)
print("3333")
task_json = crawler.CrawlTaskJson(job_core.name,urls)
task_json_str = task_json.get_json()
redis_tools.QUEUE.put(task_json_str)
print("4444")
import time 
time.sleep(1000)
#%%
print("OVER")