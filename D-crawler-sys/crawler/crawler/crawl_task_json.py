__all__=(
    "CrawlTaskJson",
)

import json 

class CrawlTaskJson:
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