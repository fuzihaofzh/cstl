# CSTL : The C++ Standard Template Library (STL) for Python

In this `cstl` tool, we wrap several C++ STL containers to use in Python. The containers use native C++ implementation and does not have the [Copy-on-Write issue](#copy-on-Write-issue-in-python) like native `list`, and `dict` in Python (Someone refers to it as memory leakage in multiprocessing which always happens in all Python native objects with ref count). Though it is designed to solve the CoW issue, it can also be used in scenarios where a standard C++ container is needed.

## Install
Install from `pip`:
```
pip install cstl
```
Build from source:
```
conda install swig # You should first install swig
git clone https://github.com/fuzihaofzh/cstl.git
cd cstl
./build.sh
python setup.py install --single-version-externally-managed --record files.txt
```

For users on windows or MacOS. Please compile from the source.

## Usage 
```python
import cstl

# Directly covert containers from python
v = cstl.frompy({"1":[1,2,3], "2":[4,5,6]}) # convert python object to cstl object
v["1"][2] = 10 # access cstl object
pv = cstl.topy(v) # convert cstl object to python object 
print(pv)

# You can also explictly specify the type
vec = cstl.VecInt([1,2,3,4,5,6,7])
print(vec[2])      #3

vec[2] = 1
print(vec[2])      #1

vec.append(10)
print(vec[-1])     #10

# User should explictly convert std::vector into list as follows:
print(list(vec))   #[1, 2, 1, 4, 5, 6, 7, 10] 

vmif = cstl.VecMapIntFloat([{1:3.4},{4:5.5}])
print(vmif[0][1])  #3.4000000953674316
```

Please refer to more usage in `test/test.py`.

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


We also support nested container, namely, structure like `std::unordered_map< std::string,std::vector< bool > > ` is supported. Currently, at most 3 nested layers are supported. If you want to support more layers, simply uncomment the line `full.update(fourth)` in `generate_swig.py` and compile from the source. But please note the the generated files could be very large. We suggest modifying the generated `cstl/cstl.i` file to only keep the containers you will use and compile the lib manually.

Please be noted that if you want to pass a Python set to set in `cstl`, you should first convert it into a list. This is a [known issue](https://stackoverflow.com/questions/73900661/using-swig-python-wrapper-argument-2-of-type-stdunordered-set-stdstring) for swig, let's see whether it will be resolved soon. 

## Speed Comparison

|           |   python |   numpy |   cstl |   pytorch |
|:----------|---------:|--------:|-------:|----------:|
| add1      |    0.19  |   0.28  |  0.911 |     4.714 |
| read      |    0.161 |   0.2   |  0.526 |     1.033 |
| sliceread |    0.327 |   0.264 |  0.683 |     1.381 |
| append    |    0.204 |  >10    |  0.351 |    >10    |
| pop       |   >10    |  >10    |  0.595 |    >10    |

It can be concluded from the table that cstl is slower than python native list and numpy in basic tasks. However, it is faster in some specific task. Most importantly, it sovles the CoW issue and provide more data structures than numpy.

## Copy-on-Write Issue in Python
[Copy-on-write](https://en.wikipedia.org/wiki/Copy-on-write) is a feature and not a bug for Python. Usually, in python multiprocessing, if we have a large data shared by each process, we will see as the program runs, the engaged memory grows gradually and finally occupy all the machine's memory and raise a Memory Error. Someone refers to it as memory leaky in the multiprocess. However, this is caused by a feature of Python. It is because, in multi-processing programs, the shared object will be copied to each process if they access the data. However, if the data is large and we use several processes, the memory cannot hold a separate copy for each process. This cannot be solved in Python as all Python's native structures with ref count have such problems (feature?). A more detailed discussion can be found at https://github.com/pytorch/pytorch/issues/13246 . Many other containers like pytorch, numpy. However, they do not support data structure like nested map.

## Supported STL Containers List
We support the following nested containers. If you need more than 3 layers of nested containers please refer to [Supported Containers](#supported-containers)

See [All Supported Containers](./supported_containers.md) for details of other containers.