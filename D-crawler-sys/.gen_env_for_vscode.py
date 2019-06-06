import os 

with open("env.sh","r") as fr:
    content=fr.read()

import re 

# 不过这一句对注释掉的部分还是生效，所以说不够完美
pattern=r"export\s+(\w+)\s*\=.*"
ls=re.findall(pattern,content)

ls=" ".join(ls)
print(ls)