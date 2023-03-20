from torch.utils.data import Dataset, DataLoader
import numpy as np
import torch
import copy
from collections import OrderedDict
import gc
from multiprocessing import Manager
import sys
import CSTL
from tqdm.auto import tqdm

class MyDict(object):
    def __init__(self, d = {}):
        self.cnt = 0
        if type(d) is dict:
            for key in d:
                setattr(self, self._convert_key(key), d[key])
                self.cnt += 1
        elif type(d) is set:
            for key in d:
                setattr(self, self._convert_key(key), None)
                self.cnt += 1
        elif type(d) is list:
            for key in range(len(d)):
                setattr(self, self._convert_key(key), d[key])
                self.cnt += 1
        
    def __getitem__(self, key):
        return getattr(self, self._convert_key(key))

    def __setitem__(self, key, value):
        if not hasattr(self, self._convert_key(key)):
            self.cnt += 1
        setattr(self, self._convert_key(key), value)

    def __contains__(self, key):
        return hasattr(self, self._convert_key(key))

    def __len__(self):
        return self.cnt

    def _convert_key(self, key):
        if type(key) is str:
            return "str" + key
        else:
            return "int" + str(key)


class DataIter(Dataset):
    def __init__(self):
        cnt = 24000000
        self.cnt = cnt
        #self.data = np.array([x for x in range(cnt)]) # Good
        self.data = [x for x in range(cnt)] #Leaky
        #self.data = "1" * cnt # Good
        #self.data = {x : x for x in range(cnt)} # Leaky
        #self.data = OrderedDict({x : x for x in range(cnt)}) # Leaky
        #self.data = MyDict({x : x for x in range(cnt)}) # Leaky??
        #self.data = np.array([{x : x for x in range(cnt)}]) # Leaky
        #self.data = {"1": np.array([x for x in range(cnt)])}# Good
        #self.data = tuple([x for x in range(cnt)])# Leaky
        #self.data = Manager().list([x for x in range(cnt)])# too slow
        #self.data = np.array([str(x) for x in range(cnt)]).astype(np.string_)# Good, save memory than directly save var in numpy
        #self.data = Foo(5)
        #self.data = cmap.IntMap()
        #for i in range(24000000):
        #    self.data.set(i, i)
        self.data = CSTL.VecInt(range(24000000)) # Good
        
    def __len__(self):
        #return len(self.data.item())
        return self.cnt

    def __getitem__(self, idx):
        """
        if not hasattr(self, "ddata"): # Good
            self.ddata = copy.deepcopy(set(self.data))
            #del self.data
            gc.collect()#"""
        data = self.data[idx]
        data = np.array([int(data)], dtype=np.int64)
        return torch.tensor(data)


train_data = DataIter()
train_loader = DataLoader(train_data, batch_size=300,
                          shuffle=True,
                          drop_last=True,
                          pin_memory=False,
                          num_workers=18)

for i, item in tqdm(enumerate(train_loader)):
    torch.cuda.empty_cache()
    if i % 1000 == 0:
        print(i)