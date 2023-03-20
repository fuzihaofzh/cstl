import CSTL
import time

total = 1000000

def rand_access_test(lst):
    st = time.time()
    for i in range(len(lst)):
        lst[i] += 1
    print(time.time() - st)

def find_element_test(lst):
    st = time.time()
    lst.find(9999999)
    print(time.time() - st)

plst = list(range(1000000))
rand_access_test(plst)
vec_int = CSTL.VecInt(range(1000000))
rand_access_test(vec_int)

find_element_test(plst)
find_element_test(vec_int)
