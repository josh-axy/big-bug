__all__=(
    "print_exception",
    "print_info",
)

from .timetools import get_cur_timeStamp

def print_exception(execption:Exception):
    '''
        用于打印异常
        当前时间 + 异常类型 + 异常内容
    '''
    print(get_cur_timeStamp(), "{}:".format(type(execption)), execption)

def print_info(string:str):
    '''
        用于打印普通字符串
        当前时间 + 字符串内容
    '''
    print(get_cur_timeStamp(), string)