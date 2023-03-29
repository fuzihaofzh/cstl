python generate_swig.py
cd cstl
PYINCLUDE=$(python -c "from sysconfig import get_paths as gp; print(gp()['include'])")
swig -c++ -python -py3 cstl.i
g++ -std=c++11 -fPIC -c -x c++ cstl_wrap.cxx -o cstl_wrap.o -I$PYINCLUDE -O3
g++ -shared cstl_wrap.o -o _cstl.so -O3
cd ..
python post_process.py
