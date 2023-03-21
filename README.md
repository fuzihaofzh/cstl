# CSTL : The C++ Standard Template Library (STL) for Python

In this `cstl` tool, we wrap several C++ STL containers to use in Python. The containers use native C++ implementation and will not have the [Copy-on-Write issue](#copy-on-Write-issue-in-python) like native `list`, and `dict` in Python (Someone refers to it as memory leakage in multiprocessing which always happens in all Python native objects with ref count). Though it is designed to solve the CoW issue, it can also be used in scenarios where a standard C++ container is needed.

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

## Usage 
```python
import cstl
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


We also support nested container, namely, structure like `std::unordered_map< std::string,std::vector< bool > > ` is supported. Currently, at most 2 nested layers are supported. If you want to support more layers, simply uncomment the line `full.update(third)` in `generate_swig.py` and compile from the source. But please note the the generated files could be very large.

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
We support the following nested containers. If you need more than 2 layers of nested containers please refer to [Supported Containers](#supported-containers)

|cstl name|C++ class|
|---|---|
| VecInt | `std::vector<int> ` |
| VecStr | `std::vector<std::string> ` |
| VecFloat | `std::vector<float> ` |
| VecDouble | `std::vector<double> ` |
| VecBool | `std::vector<bool> ` |
| VecLong | `std::vector<std::int64_t> ` |
| SetInt | `std::unordered_set<int> ` |
| SetStr | `std::unordered_set<std::string> ` |
| SetLong | `std::unordered_set<std::int64_t> ` |
| MapIntInt | `std::unordered_map<int, int> ` |
| MapIntStr | `std::unordered_map<int, std::string> ` |
| MapIntFloat | `std::unordered_map<int, float> ` |
| MapIntDouble | `std::unordered_map<int, double> ` |
| MapIntBool | `std::unordered_map<int, bool> ` |
| MapIntLong | `std::unordered_map<int, std::int64_t> ` |
| MapStrInt | `std::unordered_map<std::string, int> ` |
| MapStrStr | `std::unordered_map<std::string, std::string> ` |
| MapStrFloat | `std::unordered_map<std::string, float> ` |
| MapStrDouble | `std::unordered_map<std::string, double> ` |
| MapStrBool | `std::unordered_map<std::string, bool> ` |
| MapStrLong | `std::unordered_map<std::string, std::int64_t> ` |
| MapLongInt | `std::unordered_map<std::int64_t, int> ` |
| MapLongStr | `std::unordered_map<std::int64_t, std::string> ` |
| MapLongFloat | `std::unordered_map<std::int64_t, float> ` |
| MapLongDouble | `std::unordered_map<std::int64_t, double> ` |
| MapLongBool | `std::unordered_map<std::int64_t, bool> ` |
| MapLongLong | `std::unordered_map<std::int64_t, std::int64_t> ` |
| VecVecInt | `std::vector<std::vector<int> > ` |
| VecVecStr | `std::vector<std::vector<std::string> > ` |
| VecVecFloat | `std::vector<std::vector<float> > ` |
| VecVecDouble | `std::vector<std::vector<double> > ` |
| VecVecBool | `std::vector<std::vector<bool> > ` |
| VecVecLong | `std::vector<std::vector<std::int64_t> > ` |
| VecSetInt | `std::vector<std::unordered_set<int> > ` |
| VecSetStr | `std::vector<std::unordered_set<std::string> > ` |
| VecSetLong | `std::vector<std::unordered_set<std::int64_t> > ` |
| VecMapIntInt | `std::vector<std::unordered_map<int, int> > ` |
| VecMapIntStr | `std::vector<std::unordered_map<int, std::string> > ` |
| VecMapIntFloat | `std::vector<std::unordered_map<int, float> > ` |
| VecMapIntDouble | `std::vector<std::unordered_map<int, double> > ` |
| VecMapIntBool | `std::vector<std::unordered_map<int, bool> > ` |
| VecMapIntLong | `std::vector<std::unordered_map<int, std::int64_t> > ` |
| VecMapStrInt | `std::vector<std::unordered_map<std::string, int> > ` |
| VecMapStrStr | `std::vector<std::unordered_map<std::string, std::string> > ` |
| VecMapStrFloat | `std::vector<std::unordered_map<std::string, float> > ` |
| VecMapStrDouble | `std::vector<std::unordered_map<std::string, double> > ` |
| VecMapStrBool | `std::vector<std::unordered_map<std::string, bool> > ` |
| VecMapStrLong | `std::vector<std::unordered_map<std::string, std::int64_t> > ` |
| VecMapLongInt | `std::vector<std::unordered_map<std::int64_t, int> > ` |
| VecMapLongStr | `std::vector<std::unordered_map<std::int64_t, std::string> > ` |
| VecMapLongFloat | `std::vector<std::unordered_map<std::int64_t, float> > ` |
| VecMapLongDouble | `std::vector<std::unordered_map<std::int64_t, double> > ` |
| VecMapLongBool | `std::vector<std::unordered_map<std::int64_t, bool> > ` |
| VecMapLongLong | `std::vector<std::unordered_map<std::int64_t, std::int64_t> > ` |
| MapIntVecInt | `std::unordered_map<int, std::vector<int> > ` |
| MapIntVecStr | `std::unordered_map<int, std::vector<std::string> > ` |
| MapIntVecFloat | `std::unordered_map<int, std::vector<float> > ` |
| MapIntVecDouble | `std::unordered_map<int, std::vector<double> > ` |
| MapIntVecBool | `std::unordered_map<int, std::vector<bool> > ` |
| MapIntVecLong | `std::unordered_map<int, std::vector<std::int64_t> > ` |
| MapIntSetInt | `std::unordered_map<int, std::unordered_set<int> > ` |
| MapIntSetStr | `std::unordered_map<int, std::unordered_set<std::string> > ` |
| MapIntSetLong | `std::unordered_map<int, std::unordered_set<std::int64_t> > ` |
| MapIntMapIntInt | `std::unordered_map<int, std::unordered_map<int, int> > ` |
| MapIntMapIntStr | `std::unordered_map<int, std::unordered_map<int, std::string> > ` |
| MapIntMapIntFloat | `std::unordered_map<int, std::unordered_map<int, float> > ` |
| MapIntMapIntDouble | `std::unordered_map<int, std::unordered_map<int, double> > ` |
| MapIntMapIntBool | `std::unordered_map<int, std::unordered_map<int, bool> > ` |
| MapIntMapIntLong | `std::unordered_map<int, std::unordered_map<int, std::int64_t> > ` |
| MapIntMapStrInt | `std::unordered_map<int, std::unordered_map<std::string, int> > ` |
| MapIntMapStrStr | `std::unordered_map<int, std::unordered_map<std::string, std::string> > ` |
| MapIntMapStrFloat | `std::unordered_map<int, std::unordered_map<std::string, float> > ` |
| MapIntMapStrDouble | `std::unordered_map<int, std::unordered_map<std::string, double> > ` |
| MapIntMapStrBool | `std::unordered_map<int, std::unordered_map<std::string, bool> > ` |
| MapIntMapStrLong | `std::unordered_map<int, std::unordered_map<std::string, std::int64_t> > ` |
| MapIntMapLongInt | `std::unordered_map<int, std::unordered_map<std::int64_t, int> > ` |
| MapIntMapLongStr | `std::unordered_map<int, std::unordered_map<std::int64_t, std::string> > ` |
| MapIntMapLongFloat | `std::unordered_map<int, std::unordered_map<std::int64_t, float> > ` |
| MapIntMapLongDouble | `std::unordered_map<int, std::unordered_map<std::int64_t, double> > ` |
| MapIntMapLongBool | `std::unordered_map<int, std::unordered_map<std::int64_t, bool> > ` |
| MapIntMapLongLong | `std::unordered_map<int, std::unordered_map<std::int64_t, std::int64_t> > ` |
| MapStrVecInt | `std::unordered_map<std::string, std::vector<int> > ` |
| MapStrVecStr | `std::unordered_map<std::string, std::vector<std::string> > ` |
| MapStrVecFloat | `std::unordered_map<std::string, std::vector<float> > ` |
| MapStrVecDouble | `std::unordered_map<std::string, std::vector<double> > ` |
| MapStrVecBool | `std::unordered_map<std::string, std::vector<bool> > ` |
| MapStrVecLong | `std::unordered_map<std::string, std::vector<std::int64_t> > ` |
| MapStrSetInt | `std::unordered_map<std::string, std::unordered_set<int> > ` |
| MapStrSetStr | `std::unordered_map<std::string, std::unordered_set<std::string> > ` |
| MapStrSetLong | `std::unordered_map<std::string, std::unordered_set<std::int64_t> > ` |
| MapStrMapIntInt | `std::unordered_map<std::string, std::unordered_map<int, int> > ` |
| MapStrMapIntStr | `std::unordered_map<std::string, std::unordered_map<int, std::string> > ` |
| MapStrMapIntFloat | `std::unordered_map<std::string, std::unordered_map<int, float> > ` |
| MapStrMapIntDouble | `std::unordered_map<std::string, std::unordered_map<int, double> > ` |
| MapStrMapIntBool | `std::unordered_map<std::string, std::unordered_map<int, bool> > ` |
| MapStrMapIntLong | `std::unordered_map<std::string, std::unordered_map<int, std::int64_t> > ` |
| MapStrMapStrInt | `std::unordered_map<std::string, std::unordered_map<std::string, int> > ` |
| MapStrMapStrStr | `std::unordered_map<std::string, std::unordered_map<std::string, std::string> > ` |
| MapStrMapStrFloat | `std::unordered_map<std::string, std::unordered_map<std::string, float> > ` |
| MapStrMapStrDouble | `std::unordered_map<std::string, std::unordered_map<std::string, double> > ` |
| MapStrMapStrBool | `std::unordered_map<std::string, std::unordered_map<std::string, bool> > ` |
| MapStrMapStrLong | `std::unordered_map<std::string, std::unordered_map<std::string, std::int64_t> > ` |
| MapStrMapLongInt | `std::unordered_map<std::string, std::unordered_map<std::int64_t, int> > ` |
| MapStrMapLongStr | `std::unordered_map<std::string, std::unordered_map<std::int64_t, std::string> > ` |
| MapStrMapLongFloat | `std::unordered_map<std::string, std::unordered_map<std::int64_t, float> > ` |
| MapStrMapLongDouble | `std::unordered_map<std::string, std::unordered_map<std::int64_t, double> > ` |
| MapStrMapLongBool | `std::unordered_map<std::string, std::unordered_map<std::int64_t, bool> > ` |
| MapStrMapLongLong | `std::unordered_map<std::string, std::unordered_map<std::int64_t, std::int64_t> > ` |
| MapLongVecInt | `std::unordered_map<std::int64_t, std::vector<int> > ` |
| MapLongVecStr | `std::unordered_map<std::int64_t, std::vector<std::string> > ` |
| MapLongVecFloat | `std::unordered_map<std::int64_t, std::vector<float> > ` |
| MapLongVecDouble | `std::unordered_map<std::int64_t, std::vector<double> > ` |
| MapLongVecBool | `std::unordered_map<std::int64_t, std::vector<bool> > ` |
| MapLongVecLong | `std::unordered_map<std::int64_t, std::vector<std::int64_t> > ` |
| MapLongSetInt | `std::unordered_map<std::int64_t, std::unordered_set<int> > ` |
| MapLongSetStr | `std::unordered_map<std::int64_t, std::unordered_set<std::string> > ` |
| MapLongSetLong | `std::unordered_map<std::int64_t, std::unordered_set<std::int64_t> > ` |
| MapLongMapIntInt | `std::unordered_map<std::int64_t, std::unordered_map<int, int> > ` |
| MapLongMapIntStr | `std::unordered_map<std::int64_t, std::unordered_map<int, std::string> > ` |
| MapLongMapIntFloat | `std::unordered_map<std::int64_t, std::unordered_map<int, float> > ` |
| MapLongMapIntDouble | `std::unordered_map<std::int64_t, std::unordered_map<int, double> > ` |
| MapLongMapIntBool | `std::unordered_map<std::int64_t, std::unordered_map<int, bool> > ` |
| MapLongMapIntLong | `std::unordered_map<std::int64_t, std::unordered_map<int, std::int64_t> > ` |
| MapLongMapStrInt | `std::unordered_map<std::int64_t, std::unordered_map<std::string, int> > ` |
| MapLongMapStrStr | `std::unordered_map<std::int64_t, std::unordered_map<std::string, std::string> > ` |
| MapLongMapStrFloat | `std::unordered_map<std::int64_t, std::unordered_map<std::string, float> > ` |
| MapLongMapStrDouble | `std::unordered_map<std::int64_t, std::unordered_map<std::string, double> > ` |
| MapLongMapStrBool | `std::unordered_map<std::int64_t, std::unordered_map<std::string, bool> > ` |
| MapLongMapStrLong | `std::unordered_map<std::int64_t, std::unordered_map<std::string, std::int64_t> > ` |
| MapLongMapLongInt | `std::unordered_map<std::int64_t, std::unordered_map<std::int64_t, int> > ` |
| MapLongMapLongStr | `std::unordered_map<std::int64_t, std::unordered_map<std::int64_t, std::string> > ` |
| MapLongMapLongFloat | `std::unordered_map<std::int64_t, std::unordered_map<std::int64_t, float> > ` |
| MapLongMapLongDouble | `std::unordered_map<std::int64_t, std::unordered_map<std::int64_t, double> > ` |
| MapLongMapLongBool | `std::unordered_map<std::int64_t, std::unordered_map<std::int64_t, bool> > ` |
| MapLongMapLongLong | `std::unordered_map<std::int64_t, std::unordered_map<std::int64_t, std::int64_t> > ` |