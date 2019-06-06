__all__=(
    "println_with_ch_around",
    "merge_lines",
)

def println_with_ch_around(msg,ch:str="+",ch_repeat_time=20):
    tmp=ch*ch_repeat_time
    print("{around} {msg} {around}".format(msg=msg,around=tmp))

def merge_lines(*string_ls:list):
    return " ".join(string_ls)