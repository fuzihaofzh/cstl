python generate_swig.py
cd CSTL
PYINCLUDE=$(python -c "from sysconfig import get_paths as gp; print(gp()['include'])")
swig -c++ -python -py3 CSTL.i
g++ -std=c++11 -fPIC -c -x c++ CSTL_wrap.cxx -o CSTL_wrap.o -I$PYINCLUDE -O3
g++ -shared CSTL_wrap.o -o _CSTL.so -O3
