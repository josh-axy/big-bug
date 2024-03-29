import threading
import functools 
import collections

class LockedIterator():
    '''
        加锁的迭代器，使迭代线程安全
    '''
    '''
        python 3.x 的 LockedIterator 写法
    '''
    def __init__(self,it):
        self.lock=threading.Lock()
        self.it=it.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        self.lock.acquire()
        try:
            return next(self.it)
        finally:
            self.lock.release()


def thread_safe_generator(gen_fn):
    '''
        用于构造线程安全生成器的装饰器
    '''
    @functools.wraps(gen_fn)
    def wrapper(*args,**kw):
        return LockedIterator(gen_fn(*args,**kw))
    return wrapper
    
