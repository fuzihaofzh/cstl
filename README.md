# CSTL : The C++ Standard Template Library (STL) for Python

In this `CSTL` tool, we wrap several C++ STL containers to use in Python. The containers use native C++ implementation and will not have the [copy on write][https://en.wikipedia.org/wiki/Copy-on-write] issue like native `list`, and `dict` in Python. Though it is designed to solve the CoW issue, it can also be used in scenarios where a standard C++ container is needed.

## Install
Install from `pip`:
```
pip install CSTL
```
Build from source:
```
git clone https://github.com/fuzihaofzh/CSTL.git
cd CSTL
./build.sh
python setup.py install
```

## Usage 
```python
import CSTL
vec = CSTL.VecInt([1,2,3,4,5,6,7])
print(vec[2])      #3
vec[2] = 1
print(vec[2])      #1
vec.append(10)
print(vec[-1])     #10
print(list(vec))   #[1, 2, 1, 4, 5, 6, 7, 10]
```

## Supported Datatype

We support the following data types as the elements in the containers
|Python Type|C++ Type| Can be dict key|
|---|---|---|
|int|int|Yes|
|int|std::int64|Yes|
|str|std::string|Yes|
|float|float|No|
|double|double|No|
|bool|bool|No|

## Supported Containers
The supported containers are listed as follows
|Python Structure|C++ Container| 
|---|---|
|list|std::vector|
|dict|std::unordered_map|
|set|std::unordered_set|

We also support nested container, namely, structure like `std::unordered_map< std::string,std::unordered_map< std::string,std::vector< bool > > >` is supported. Currently, at most 3 nested layers are supported.

## Copy on Write Issue in Python
This is a feature not a bug for Python. In multi-processing programs, the shared object will be copied to each process if they access the data. However, if the data is large and we use several processes, the memory cannot hold a separate copy for each process. This cannot be solved in Python as all Python's native structures with ref count have such problems. A more detailed discussion can be found at https://github.com/pytorch/pytorch/issues/13246 .




