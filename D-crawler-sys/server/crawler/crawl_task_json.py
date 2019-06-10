__all__=(
    "CrawlTaskJson",
)

import json 

class CrawlTaskJson:
    '''
        爬虫任务的json形式如下:
        {
            "job_name":"hahaha",
            "urls":[
                "https://haha.hahaha.ha/xxx",
                "https://haha.hahaha.ha/yyy",
            ]
        }
        这个json作为一个整体加入队列，也作为一个任务分配单元分配给爬虫端
        所以 urls 一次不要放太多
    '''
    @classmethod
    def from_json_str(cls,json_str:str):
        x = json.loads(json_str)
        obj = cls(x["job_name"],x["urls"])
        return obj

    def __init__(self,crawl_job_name:str,urls:list):
        assert isinstance(crawl_job_name,str) and isinstance(urls,list)
        assert bool(crawl_job_name) and bool(urls) # 判空
        self.job_name = crawl_job_name
        self.urls = urls 

    def get_json(self)->str:
        x = {
            "job_name":self.job_name,
            "urls":self.urls,
        }
        _json_str = json.dumps(x)
        return _json_str