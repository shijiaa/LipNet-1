# extract a sublist of size size starting from index from l (circular list)
def get_list_safe(l, index, size):
    ret = l[index:index+size]
    while size - len(ret) > 0:
        ret += l[0:size - len(ret)]
    return ret
