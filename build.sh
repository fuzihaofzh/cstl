python generate_swig.py
cd CSTL
swig -c++ -python -py3 CSTL.i
g++ -std=c++11 -fPIC -c -x c++ CSTL_wrap.cxx -o CSTL_wrap.o -I/home/zf268/programs/miniconda3/include/python3.9 
g++ -shared CSTL_wrap.o -o _CSTL.so
