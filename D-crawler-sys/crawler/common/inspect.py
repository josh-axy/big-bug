import inspect
from collections.abc import Callable

def get_params(_callable:Callable):
    '''
        获取一个 Callable 的参数名
        (Callable 一般指 function, method, 实现了__call__的 class 的 instance, 以及 class (构造函数))
    '''
    params = (ele for ele in inspect.signature(_callable).parameters)
    return params