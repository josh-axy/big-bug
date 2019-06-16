# D-crawler-sys (BIG BUG)

#### 介绍
大数据软件技术大作业：分布式爬虫 BIG BUG
使用了 redis, hbase

一开始还考虑到使用 zookeeper 做状态管理，用redis布隆过滤器插件做重复url的剔除。

但因为时间不够放弃了。

最后提交时，很多部分没有做好。
比如爬虫job规则的更新，数据库里的更新了，但是 LRU 缓存没有跟上。



#### 安装教程

1. 分布式安装配置 redis，hdfs，hbase （其中redis-cluster的配置相当的繁琐）

2. 安装python3.6，pypi

3. 找到 pip-requirements.txt 文件，执行命令： `pip install -r requriements.txt`

   ```
   aiohttp==3.3.2
   happybase==1.2.0
   redis==3.2.1
   rediscluster==0.5.3
   selenium==3.141.0
   Beaker==1.10.1
   bottle==0.12.16
   ```
   
   

#### 使用注意点

1. 使用前先对 config 文件夹下各文件进行配置，主要是配置 redis, hbase-thrift 的 host 和 端口号。

2. 要特别注意 redis-conf.json文件

   single_node_mode 为 true 时，使用单机配置，即 "host","ip"；为 false 使用集群配置，即 "master_nodes"

```json
{
    "single_node_mode":false,
    "host":"localhost", 
    "port":6379,
    "decode_responses":true,
    "namespace":"crawler",
    "queue_name":"queue",
    "close_set_name":"close_set",
    "master_nodes":[
        {"host":"192.168.133.128","port":"7001"},
		{"host":"192.168.133.128","port":"7002"},
		{"host":"192.168.133.128","port":"7003"}
    ]
}
```
3. 在项目目录运行 `python -m http.server` 命令，在该目录启动web服务器，主页为该目录下的 index.html。输出的端口号即之后web页面的端口号。
4. 运行 `bash run-crawler.sh` 启动爬虫端；运行 `bash run-server.sh` 启动服务端。


