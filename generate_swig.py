import os
ktypes = {"Int" : "int", "Str" : "std::string", "Long" : "std::int64_t"}
bvtypes = {"Int" : {"cname" : "int"}, "Str" : {"cname" : "std::string"}, "Float" : {"cname" : "float"}, "Double" : {"cname" : "double"}, "Bool" : {"cname" : "bool"} , "Long" : {"cname" : "std::int64_t"}}

header = """%module cstl

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
        conversion = f"$result = swig::from(static_cast< std::vector<{types[t]['cname']},std::allocator< {types[t]['cname']} > >* >($1));"
        res["Vec" + t] = {"cname" : f"std::vector<{types[t]['cname']}> ", "typemap" : f"%typemap(out) std::vector<{types[t]['cname']} >::value_type & {{\n    {types[t]['conversion']}\n}}" if 'conversion' in types[t] else "", "conversion" : conversion}
    return res

def make_map(keys, vtypes):
    res = {}
    for key in keys:
        for t in vtypes:
            conversion = f"resultobj = swig::from(static_cast< std::unordered_map< {keys[key]}, {vtypes[t]['cname']},std::hash< {keys[key]} >,std::equal_to< {keys[key]} >,std::allocator< std::pair< {keys[key]} const,{vtypes[t]['cname']} > > > * >(result));"
            res["Map" + key + t] = {"cname" : f"std::unordered_map<{keys[key]}, {vtypes[t]['cname']}> ", "typemap" : f"%typemap(out) std::unordered_map<{keys[key]}, {vtypes[t]['cname']} >::mapped_type & {{\n    {vtypes[t]['conversion']}\n}}" if "conversion" in vtypes[t] else "", "conversion" : conversion}
    return res

def make_set(types):
    res = {}
    for t in types:
        conversion = f"$result = swig::from(static_cast< std::unordered_set< {types[t]},std::hash< {types[t]} >,std::equal_to< {types[t]} >,std::allocator< {types[t]} > > * >(result));"
        res["Set" + t] = {"cname" : f"std::unordered_set<{types[t]}> ", "typemap" : "", "conversion" : conversion}
    return res

def render(tmap):
    return [f"{tmap[t]['typemap']}\n%template({t}) {tmap[t]['cname']};\n" for t in tmap]

first = {}
first.update(make_vec(bvtypes))
first.update(make_set(ktypes))
first.update(make_map(ktypes, bvtypes))

second = {}
second.update(make_vec(first))
second.update(make_map(ktypes, first))

third = {}
third.update(make_vec(second))
third.update(make_map(ktypes, second))

fourth = {}
fourth.update(make_vec(third))
fourth.update(make_map(ktypes, third))

full = {}
full.update(first)
full.update(second)
full.update(third)
#full.update(fourth)

os.system("mkdir cstl -p")
content = header + "\n".join(render(full))
open("cstl/cstl.i", "w").write(content)


open("cstl/cstl.i", "w").write(content)
open("cstl/__init__.py", "w").write("from cstl.version import __version__\nfrom cstl.cstl import *")
os.system("cp version.py cstl/version.py")




supported_containers_header = """
|cstl name|C++ class|
|---|---|
"""
md = []
for f in full:
    md.append(f"| {f} | `{full[f]['cname']}` |")
open("supported_containers.md", "w").write(supported_containers_header + "\n".join(md))


