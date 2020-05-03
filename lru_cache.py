import collections
import functools

from random import randint

class lru_cache_obj(object):
    cache_size = 0

    def __init__(self, size):
        if size <= 0:
            exit(0)
        self.cache_size = size
        self.cache_dict = collections.OrderedDict()

    def set(self, k, v):
        try:
            self.cache_dict.pop(k)
        except KeyError:
            if len(self.cache_dict) >= self.cache_size:
                self.cache_dict.popitem(last=False)
        self.cache_dict[k] = v
        # print(self.cache_dict[k])

    def get(self, k):
        try:
            value = self.cache_dict[k]
            self.cache_dict.pop(k)
            self.cache_dict[k] = value
            # for key in self.cache_dict:
            #     print("dict {}".format(key)) 
            return value
        except KeyError:
            return -1

    def delete(self, k):
        try:
            self.cache_dict.pop(k)
            return k
        except KeyError:
            return -1

def lru_cache_test():
    c = lru_cache(5)

    for i in range(9,0,-1):
        c.set(i,"str")

    for i in range(50):
        r = randint(0,49)
        print("{} {}".format(r,c.get(r)))

# lru_cache_test()






