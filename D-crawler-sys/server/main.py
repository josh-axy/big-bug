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
import random, string

def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


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
    job_list = []
    result = {}
    result['success'] = True
    job_name_list = hbase_tools.get_job_list()
    for i in range(len(job_name_list)):
        tmp_dict = {}
        tmp_dict['id'] = generate_random_str(24);
        tmp_dict['job_name'] = job_name_list[i];
        job_list.append(tmp_dict)
    print(job_list)
    print(job_list is None)
    if job_list is None:
        result['success'] = False
        return result
    else:
        result['data'] = json.dumps(job_list, cls=MyEncoder)
    return result


# 创建 job_core，并存入 hbase
@route('/createJob')
def create_job():
    job_name = ''
    rules = []
    if request.method == 'POST':
        job_name = request.POST.get('job_name')
        print(job_name)
        rules = request.POST.getlist('rules')
        print(rules)
    result = {}
    result['success'] = True
    crawl_job = crawler.CrawlJobCore(job_name, rules)
    if hbase_tools.save_job(crawl_job):
        if redis_tools.CLOSE_SET.is_member(job_name):
            # 从close_set里移除该job_name
            redis_tools.CLOSE_SET.remove(job_name)
        return result
    else:
        result['success'] = False
    return result


# 创建 task 加入 redis 队列
@route('/createTask')
def create_task():
    job_name = '',
    urls = []
    if request.method == 'POST':
        job_name = request.POST.get('job_name')
        urls = request.POST.getlist('urls')
    result = {}
    result['success'] = True
    task_json = crawler.CrawlTaskJson(job_name,0,urls)
    task_json_str = task_json.get_json()
    redis_tools.QUEUE.put(task_json_str)
    return result


# 从 hbase 取出爬取结果
@route('/getResult')
def get_result():
    job_name = ''
    if request.method == 'POST':
        job_name = request.POST.get('job_name')
    result = {}
    result['success'] = True
    result_list = hbase_tools.get_job_result(job_name)
    if result_list is None:
        result['success'] = False
        return result
    else:
        result['data'] = json.dumps(result_list, cls=MyEncoder)
    return result

# 暂停job
@route('/pauseJob')
def pause_job():
    job_name = ''
    if request.method == 'POST':
        job_name = request.POST.get('job_name')
    result = {}
    result['success'] = True
    if not redis_tools.CLOSE_SET.is_member(job_name):
        # 向close_set里加入该job_name
        redis_tools.CLOSE_SET.add(job_name)
    return result

# 修改爬虫
@route('/updateJob')
def update_job():
    job_name = '',
    url = ''
    if request.method == 'POST':
        job_name = request.POST.get('job_name')
        url = request.POST.get('url')
    result = {}
    result['success'] = True
    job_core = hbase_tools.get_job_rule(job_name)
    if hbase_tools.set_job_rule(job_core):
        if not redis_tools.CLOSE_SET.is_member(job_name):
            # 向close_set里加入该job_name
            redis_tools.CLOSE_SET.remove(job_name)
        return result
    else:
        result['success'] = False
        return result
    

# # 继续爬虫
# @route('/restartJob')
# def restart_job():
#     job_name = ''
#     if request.method == 'POST':
#         job_name = request.POST.get('job_name')
#     result = {}
#     result['success'] = True
#     if not redis_tools.CLOSE_SET.is_member(job_name):
#         # 向close_set里加入该job_name
#         redis_tools.CLOSE_SET.remove(job_name)
#     return result

# （中途）终止爬虫
# 暂时没做
@route('/killCrawler')
def kill_crawler():
    job_name = ''
    if request.method == 'POST':
        job_name = request.POST.get('job_name')
    result = {}
    result['success'] = True
    if not redis_tools.CLOSE_SET.is_member(job_name):
        # 向close_set里加入该job_name
        redis_tools.CLOSE_SET.add(job_name)
    if hbase_tools.remove_job(job_name):
        return result
    else:
        result['success'] = False
        return result
    return result



# 显示当前 job 已经做完的 task 数量
# @route('/showTaskNum')
# def show_task_num():
#     result = {}
#     result['success'] = True
    
#     return result

host_num = common.args.server_conf["host"]
port_num = common.args.server_conf["port"]

run(host=host_num, port=port_num, debug=True)
