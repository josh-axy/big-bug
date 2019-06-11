#!/usr/bin/evn python
# coding=utf-8

import json
import re
from bottle import route, run, get, post, request, hook, response
from beaker.middleware import SessionMiddleware
import common
import crawler
import hbase_tools
import redis_tools


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


@hook('before_request')
def validate():
    REQUEST_METHOD = request.environ.get('REQUEST_METHOD')
    HTTP_ACCESS_CONTROL_REQUEST_METHOD = request.environ.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD')
    if REQUEST_METHOD == 'OPTIONS' and HTTP_ACCESS_CONTROL_REQUEST_METHOD:
        request.environ['REQUEST_METHOD'] = HTTP_ACCESS_CONTROL_REQUEST_METHOD


@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'


# transform str into json
@route('/jsonTest/<str>')
# {"params":{"id":222,"offset":0}}
def json_test(str):
    params = json.loads(str)
    print(params)
    return params


# 列出当前存在的 job （即job表）列表
@route('/jobList')
def job_list():
    result = {}
    result['success'] = True
    job_list = hbase_tools.get_job_list()
    print(job_list)
    print(job_list is None)
    if job_list is None:
        result['success'] = False
        return result
    else:
        result['data'] = json.dumps(job_list, cls=MyEncoder)
    return result


# 创建 job_core，并存入 hbase
@route('/createJob/<job_name>/<rules>')
def create_job(job_name:str, rules:list):
    result = {}
    result['success'] = True
    print(job_name)
    print(rules)
    json_rules = json.loads(rules)
    print(json_rules)
    print(type(json_rules))
    crawl_job = crawler.CrawlJobCore(job_name, rules)
    if hbase_tools.save_job(crawl_job):
        return result
    else:
        result['success'] = False
    return result


# 创建 task 加入 redis 队列
@route('/createTask/<job_name>/<url>')
def create_task(job_name:str, url:str):
    result = {}
    result['success'] = True
    task_json = crawler.CrawlTaskJson(job_name,0,url)
    task_json_str = task_json.get_json()
    redis_tools.QUEUE.put(task_json_str)
    return result


# 从 hbase 取出爬取结果
@route('/getResult/<job_name>')
def get_result(job_name):
    result = {}
    result['success'] = True
    result_list = hbase_tools.get_job_result(job_name)
    if result_list is None:
        result['success'] = False
        return result
    else:
        result['data'] = json.dumps(result_list, cls=MyEncoder)
    return result


# （中途）终止爬虫 job
# 暂时没做
@route('/killCrawler/<job_name>')
def kill_crawler(job_name):
    result = {}
    result['success'] = True
    if hbase_tools.remove_job(job_name):
        return result
    else:
        result['success'] = False
        return result
    return result


# 根据 url 列表文件和 job 名字向 redis 队列里添加task
# @route('/addTask/<job_name>/<url>')
# def add_task(job_name, url):
#     result = {}
#     result['success'] = True
    
#     return result


# 显示当前 job 已经做完的 task 数量
# @route('/showTaskNum')
# def show_task_num():
#     result = {}
#     result['success'] = True
    
#     return result


run(host='localhost', port=9092, debug=True)
