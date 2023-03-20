import os
ktypes = {"Int" : "int", "Str" : "std::string", "Long" : "std::int64_t"}
vtypes = {"Int" : "int", "Str" : "std::string", "Float" : "float", "Double" : "double", "Bool" : "bool" , "Long" : "std::int64_t"}

header = """%module CSTL

%{
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
        res["Vec" + t] = f"std::vector<{types[t]} >"
    return res

def make_map(keys, types):
    res = {}
    for key in keys:
        for t in types:
            res["Map" + key + t] = f"std::unordered_map<{keys[key]}, {types[t]} >"
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


content = header + "\n".join(render(first)) + "\n".join(render(second)) + "\n".join(render(third))

os.system("mkdir CSTL")
open("CSTL/CSTL.i", "w").write(content)
open("CSTL/__init__.py", "w").write("from CSTL.version import __version__\nfrom CSTL.CSTL import *")
os.system("cp version.py CSTL/version.py")

