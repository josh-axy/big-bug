__all__=(
    "check_url",
)

import re 

# Django url验证 正规表达式

# url_regex = re.compile(
#  r'^(?:http|ftp)s?://' # http://or https://
#  r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?.)+(?:[A-Z]{2,6}.?|[A-Z0-9-]{2,}.?)|' #domain...
#  r'localhost|' #localhost...
#  r'd{1,3}.d{1,3}.d{1,3}.d{1,3})' #.. .or ip
#  r'(?::d+)?' # optional port
#  r'(?:/?|[/?]S+)$', re.IGNORECASE)

url_regex = re.compile(
 r'^(?:http)s?://' # http://or https://
 r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?.)+(?:[A-Z]{2,6}.?|[A-Z0-9-]{2,}.?)|' #domain...
 r'localhost|' #localhost...
 r'd{1,3}.d{1,3}.d{1,3}.d{1,3})' #.. .or ip
 r'(?::d+)?' # optional port
 r'(?:/?|[/?]S+)$', re.IGNORECASE)

def check_url(url:str)->bool:
    '''
        检查url的合法性
    '''
    return bool(url_regex.match(url))


if __name__=="__main__":
    url = "ftps://www.baidu.com"
    print(check_url(url))