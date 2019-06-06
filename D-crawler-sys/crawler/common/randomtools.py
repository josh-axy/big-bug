__all__=(
    "gen_random_int",
    "gen_random_int_str",
)


import random

# 形如999的数字，索引表示十进制位数
nine_nine = [0, 9, 99, 999, 9999, 99999, 999999, 9999999, 99999999, 999999999]

# 获取length长度的随机整数字符串，不足位用0填补

defaultLength = 7


def gen_random_int(length=defaultLength):
    return random.randint(0, nine_nine[length % 10])


def gen_random_int_str(length=defaultLength):
    r = gen_random_int(length)
    return str(r).zfill(length)