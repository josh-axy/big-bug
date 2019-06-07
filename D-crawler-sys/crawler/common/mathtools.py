
def clip(num, lower_boundary, upper_boundary):
    if num < lower_boundary:
        return lower_boundary
    elif num > upper_boundary:
        return upper_boundary
    return num
