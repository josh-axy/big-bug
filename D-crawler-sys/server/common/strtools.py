__all__=(
    "println_with_ch_around",
    "merge_lines",
)

def println_with_ch_around(msg,ch:str="+",ch_repeat_time=20):
    '''
       打印信息，并用 ch * ch_repeat_time 包裹
       比如 ++++++hello++++++
    '''
    tmp=ch*ch_repeat_time
    print("{around} {msg} {around}".format(msg=msg,around=tmp))

def merge_lines(*string_ls:list):
    '''
        将多个字符串用空格拼接
        一般用于拼接多行字符串
    '''
    return " ".join(string_ls)