__all__=(
    "print_exception",
    "print_info",
)

from .timetools import get_cur_timeStamp

def print_exception(execption:Exception):
    print(get_cur_timeStamp(), "{}:".format(type(execption)), execption)

def print_info(string:str):
    print(get_cur_timeStamp(), string)