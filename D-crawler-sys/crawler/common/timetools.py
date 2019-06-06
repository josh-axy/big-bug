import time
import datetime
import functools
import contextlib
import threading
from collections.abc import Callable

__all__ = (
    "get_adb_format_time",
    "timer_wrapper",
    "timer_context",
    "get_cur_timeStamp",
    "get_timeStamp",
    "delay_func",
    "loop_func",
)


defaultTimeStampFormat = '%Y-%m-%d-%H-%M-%S'
# _scheduler = sched.scheduler(time.time,time.sleep)


def get_adb_format_time(_time: float):
    '''
        06-04 22:40:33.291
        %m-%d %H:%M:%S.%3q
    '''
    # old:adb_format: MM-DD hh:mm:ss.mmm
    # <class 'time.struct_time'>
    #time.struct_time(tm_year=2019, tm_mon=6, tm_mday=4, tm_hour=22, tm_min=9, tm_sec=18, tm_wday=1, tm_yday=155, tm_isdst=0)
    d = datetime.datetime.fromtimestamp(_time)
    time_str = "{}.{:03d}".format(d.strftime(
        "%m-%d %H:%M:%S"), int(d.microsecond//1000))
    return time_str

# 计时器装饰器
def timer_wrapper(func):
    @functools.wraps(func)
    def f(*args, **kw):
        with timer_context():
            func(*args, **kw)
    return f

# 计时器上下文管理器
@contextlib.contextmanager
def timer_context(tag="timer", prefix="======", suffix="======"):
    def _print(x): return print("{prefix}{tag}:{x}{suffix}".format(
        prefix=prefix, tag=tag, x=x, suffix=suffix))
    t1 = time.time()
    _print("start_time {}".format(t1))
    yield t1
    t2 = time.time()
    using_time = t2-t1
    _print("end_time {}".format(t2))
    _print("using_time {}".format(using_time))


def get_cur_timeStamp(str_format=defaultTimeStampFormat):
    return datetime.datetime.now().strftime(str_format)


def get_timeStamp(_time, str_format=defaultTimeStampFormat):
    return datetime.datetime.fromtimestamp(_time).strftime(str_format)

# 延迟函数
def delay_func(delaySeconds, func, *args, **kw):
    # 原本这个写法似乎是阻塞的
    # return _scheduler.enter(delaySeconds,0,func,args,kw)
    threading.Timer(delaySeconds, func, *args, **kw).start()

# 循环函数
def loop_func(
        intervalSeconds,
        end_func,
        max_loop_cnt=None,
        after_func=None,
        func=None,
        *args, **kw):
    '''intervalSeconds 表示时间间隔
    end_func 表示终止函数，该函数没有参数，返回bool值，如果为True，则终止
    func 表示要循环调用的函数，*args,**kw 表示它的参数
    max_loop_cnt 表示最大循环次数,值为 None 时表示无限
    after_func 表示结束后要调用的函数
    '''
    assert isinstance(func, Callable)
    assert isinstance(end_func, Callable)

    # max_loop_cnt = kw.get("max_loop_cnt",None)
    assert max_loop_cnt is None or isinstance(max_loop_cnt, int)
    # after_func = kw.get("after_func",lambda:print("loop_func {} end".format(func.__name__)))
    assert isinstance(after_func, Callable)

    def func_wrapper(*args, **kw):
        cnt = 0
        while not end_func() and (max_loop_cnt is None or cnt < max_loop_cnt):
            time.sleep(intervalSeconds)
            cnt += 1
            try:
                func(*args, **kw)
            except Exception as e:
                print(get_cur_timeStamp(), e)
        after_func()
        return
    f_wrap = functools.partial(func_wrapper, *args, **kw)
    threading.Thread(target=f_wrap).start()
