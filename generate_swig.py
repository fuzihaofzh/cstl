import os
ktypes = {"Int" : "int", "Str" : "std::string", "Long" : "std::int64_t"}
vtypes = {"Int" : "int", "Str" : "std::string", "Float" : "float", "Double" : "double", "Bool" : "bool" , "Long" : "std::int64_t"}

header = """%module CSTL

%{
//define this to avoid automatically convert std::vector to python list. User should do it manually when needed.
#   define SWIG_PYTHON_EXTRA_NATIVE_CONTAINERS  
#include <vector>
#include <unordered_map>
#include <string>
#include <stack>
#include <queue>
%}

%include "std_vector.i"
%include "std_string.i"
%include "std_unordered_map.i"
%include "std_pair.i"
%include "std_unordered_set.i"

"""


def make_vec(types):
    res = {}
    for t in types:
        res["Vec" + t] = {"cname" : f"std::vector<{types[t]} >", "typemap" : f"%typemap(out) std::vector<{types[t]} >::value_type & {{ $result = swig::from(static_cast< std::vector< <{types[t]},std::allocator< <{types[t]} > >* >($1));}}", "value" : types[t]}
    return res

def make_map(keys, vtypes):
    res = {}
    for key in keys:
        for t in vtypes:
            res["Map" + key + t] = [f"std::unordered_map<{keys[key]}, {vtypes[t]} >", 
            f"%typemap(out) std::unordered_map< {keys[key]},{vtypes[t]} >::mapped_type & {{ $result = swig::from(static_cast< std::unordered_map< int,int,std::hash< int >,std::equal_to< int >,std::allocator< std::pair< int const,int > > >* >(result));}}"]
    return res

def make_set(types):
    res = {}
    for t in types:
        res["Set" + t] = f"std::unordered_set<{types[t]} >"
    return res

def make_queue(types):
    res = {}
    for t in types:
        res["Que" + t] = f"std::queue<{types[t]} >"
    return res

def make_stack(types):
    res = {}
    for t in types:
        res["Stk" + t] = f"std::stack<{types[t]} >"
    return res

def render(tmap):
    return [f"%template({t}) {tmap[t]};" for t in tmap]
    

first = {}
first.update(make_vec(vtypes))
first.update(make_set(ktypes))
#first.update(make_queue(vtypes))
#first.update(make_stack(vtypes))
first.update(make_map(ktypes, vtypes))

second = {}
second.update(make_vec(first))
second.update(make_map(ktypes, first))

third = {}
third.update(make_vec(second))
third.update(make_map(ktypes, second))

full = first
full.update(second)
#full.update(third)
content = header + "\n".join(render(full))


os.system("mkdir CSTL")
open("CSTL/CSTL.i", "w").write(content)
open("CSTL/__init__.py", "w").write("from CSTL.version import __version__\nfrom CSTL.CSTL import *")
os.system("cp version.py CSTL/version.py")


md = []
for f in full:
    md.append(f"| {f} | `{full[f]}` |")
open("CSTL/supported_containers.md", "w").write("\n".join(md))


