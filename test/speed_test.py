import cstl
import time
import numpy as np
from collections import defaultdict
import pandas as pd
import torch

total = 1000000

def rand_access_test(lst, func, name):
    st = time.time()
    for i in range(len(lst) - 100):
        func(lst, i, name)
        if time.time() - st > 10:
            break
    return round(time.time() - st, 3)


data = {
    "python" : list(range(total)),
    "numpy" : np.array(range(total)),
    "cstl" : cstl.VecInt(range(total)),
    "pytorch" : torch.tensor(range(total))
}

print("rand_access_test")
res = defaultdict(dict)
def add1(lst, i, name):
    lst[i] += 1
def read(lst, i, name):
    a = lst[i]
def sliceread(lst, i, name):
    a = lst[i : i + 100]
def append(lst, i, name):
    if name == "numpy":
        np.append(lst, i)
    elif name == "python":
        lst.append(i)
    elif name == "pytorch":
        lst = torch.cat([lst, torch.tensor(1).unsqueeze(0)])
    else:
        lst.push_back(i)
def pop(lst, i, name):
    if name == "cstl":
        lst.pop()
    elif name == "python":
        lst.pop(0)
    else:
        np.delete(lst, i)

    
for func in [add1, read, sliceread, append, pop]:
    for l in ["python", "numpy", "cstl", "pytorch"]:
        print(func.__name__, l)
        res[l][func.__name__] = rand_access_test(data[l], func, l)

df = pd.DataFrame(res)
print(df.to_markdown())
