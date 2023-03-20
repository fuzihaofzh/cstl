import CSTL
import time
import numpy as np

total = 1000000

def rand_access_test(lst):
    st = time.time()
    for i in range(len(lst)):
        lst[i] += 1
    print(time.time() - st)

def slice_access_test(lst):
    st = time.time()
    for i in range(len(lst)):
        b = lst[200 : 300] 
    print(time.time() - st)

def find_element_test(lst):
    st = time.time()
    lst.find(9999999)
    print(time.time() - st)

plst = list(range(1000000))
vec_int = CSTL.VecInt(range(1000000))
npa = np.array(plst)

rand_access_test(plst)
rand_access_test(vec_int)
rand_access_test(npa)

slice_access_test(plst)
slice_access_test(vec_int)
slice_access_test(npa)

