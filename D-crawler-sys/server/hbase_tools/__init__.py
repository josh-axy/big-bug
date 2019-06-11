__all__=(
    "get_job_rule",
    "set_job_rule",
    "save_job",
    "remove_job",
    "save_results",
    "get_job_result",
    "get_job_list"
)

import functools

import common
import crawler
import happybase
from . import misc

conf = common.args.hbase_conf
host = conf["hbase_thrift_host"]
port = conf["hbase_thrift_port"]
table_prefix = conf["table_prefix"]
table_prefix_separator = conf["table_prefix_separator"]
hbase_pool = happybase.ConnectionPool(
    size=3, 
    host=host, 
    port=port,
    table_prefix=table_prefix,
    table_prefix_separator=table_prefix_separator
)

# 模块对外接口，用偏函数实现
# get_job_rule = functools.partial(misc._get_job_rule,hbase_pool)
# set_job_rule = functools.partial(misc._set_job_rule,hbase_pool)
# save_job = functools.partial(misc._save_job,hbase_pool)
# remove_job = functools.partial(misc._remove_job,hbase_pool)
# save_results = functools.partial(misc._save_results,hbase_pool)


def get_job_rule(job_name) -> crawler.CrawlJobCore:
    '''
        获取 hbase 里的 crawl_job_core (爬取规则)
    '''
    return misc._get_job_rule(hbase_pool,job_name)
    

def set_job_rule(crawl_job_core)->bool:
    '''
        改变规则
    '''
    return misc._set_job_rule(hbase_pool,crawl_job_core)


def save_job(crawl_job_core)-> bool:
    '''
        存储 crawl_job_core (爬取规则) 到 hbase 里
    '''
    return misc._save_job(hbase_pool,crawl_job_core)
            

def remove_job(crawl_job_name)->bool:
    '''
        删除 job (删除job_name所对应的表)
        要想删除 hbase 的表，应该先 disable 掉它
    '''
    return misc._remove_job(hbase_pool,crawl_job_name)


def save_results(crawl_job_core,url,result_list)->bool:
    '''
        保存爬取结果到 hbase 里
        如果 result_list 为空，不进行操作
    '''
    return misc._save_results(hbase_pool,crawl_job_core,url,result_list)

def get_job_list()->list:
    '''
        获取hbase中存的job名称list
    '''
    return misc._get_job_list(hbase_pool)

def get_job_result(crawl_job_name)->list:
    '''
        获取爬虫结果
    '''
    return misc._get_job_result(hbase_pool, crawl_job_name)