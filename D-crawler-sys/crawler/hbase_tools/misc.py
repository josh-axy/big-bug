import common
import crawler
import happybase

conf = common.args.hbase_conf
column_families = conf["column_families"]
rule_row_key = conf["rule"]["row_key"]
rule_col = conf["rule"]["rule_column"]
rule_max_version = conf["rule"]["max_versions"]
results_family = conf["results"]["column_family"]
results_max_version = conf["results"]["max_versions"]


def results_col_pattern(x):
    return "{}:{}".format(results_family, x)


def _get_job_rule(pool: happybase.ConnectionPool, job_name) -> crawler.CrawlJobCore:
    '''
        获取 hbase 里的 crawl_job_core (爬取规则)
    '''
    with pool.connection() as conn:
        try:
            conn: happybase.Connection
            table = conn.table(job_name)
            row = table.row(rule_row_key, columns=[rule_col, ])
            rule = row[bytes(rule_col,encoding="utf-8")].decode("utf-8")
            # _json_str = row.values
            # print(rule)
            common.print_info("get crawl rule: {}".format(rule))
            crawl_job_core = crawler.CrawlJobCore.loads(rule)
            # TODO 键 有点问题
            return crawl_job_core
        except Exception as e:
            common.print_exception(e)
            return None
            pass
        finally:
            conn.close()  # 关闭连接

def _set_job_rule(pool: happybase.ConnectionPool, crawl_job_core)->bool:
    '''
        改变规则
    '''
    core = crawl_job_core
    with pool.connection() as conn:
        try:
            conn: happybase.Connection
            table = conn.table(core.name)
            table.put(rule_row_key, {
                rule_col: core.dumps(),
            })
            return True
        except Exception as e:
            common.print_exception(e)
            return False
            pass
        finally:
            conn.close()  # 关闭连接


def _save_job(pool: happybase.ConnectionPool, crawl_job_core)-> bool:
    '''
        存储 crawl_job_core (爬取规则) 到 hbase 里
    '''
    core = crawl_job_core
    with pool.connection() as conn:
        try:
            conn: happybase.Connection
            conn.create_table(name=core.name, families={
                rule_col: dict(max_versions=rule_max_version),
                results_family: dict(max_versions=results_max_version),
            })
            table = conn.table(core.name)
            table.put(rule_row_key, {
                rule_col: core.dumps()
            })
            return True
        except Exception as e:
            common.print_exception(e)
            return False
            pass
        finally:
            conn.close()  # 关闭连接
            

def _remove_job(pool,crawl_job_name)->bool:
    '''
        删除 job (删除job_name所对应的表)
        要想删除 hbase 的表，应该先 disable 掉它
    '''
    with pool.connection() as conn:
        try:
            conn: happybase.Connection
            conn.delete_table(crawl_job_name,disable=True)
            return True
        except Exception as e:
            common.print_exception(e)
            return False
            pass
        finally:
            conn.close()  # 关闭连接


def _save_results(pool: happybase.ConnectionPool,
                  crawl_job_core,
                  url,
                  result_list)->bool:
    '''
        保存爬取结果到 hbase 里
        如果 result_list 为空，不进行操作
    '''
    if not bool(result_list):
        return False
    core = crawl_job_core
    with pool.connection() as conn:
        try:
            conn: happybase.Connection
            table = conn.table(core.name)
            row_key = url
            table.put(row_key, {
                results_col_pattern(i): ele
                for i, ele in enumerate(result_list)
            })
            return True
        except Exception as e:
            common.print_exception(e)
            return False
            pass
        finally:
            conn.close()  # 关闭连接
            
