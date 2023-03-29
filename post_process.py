mywrapper = """
#====Wrapper====
import sys

def _get_type(pyobj):
    container_map = {"list" : "Vec", "dict" : "Map", "set" : "Set"}
    type_map = {'int': 'Int', 'str': 'Str', 'float': 'Float', 'double': 'Double', 'bool': 'Bool', 'std::int64_t': 'Long'}
    stype = type(pyobj).__name__
    if stype not in container_map:
        return type_map[stype]
    if len(pyobj) == 0:
        raise AttributeError(f"Contain Empty {stype} and cannot infer the Type. Please give a non empty list or direct use the specific class to define the object.")
    if stype == "list":
        return container_map[stype] + _get_type(pyobj[0])
    elif stype == "dict":
        k0 = list(pyobj.keys())[0]
        return container_map[stype] + _get_type(k0) + _get_type(pyobj[k0])
    elif stype == "set":
        v0 = list(pyobj)[0]
        return container_map[stype] + _get_type(v0)
        
def _convert_set(pyobj):
    container_map = {"list" : "Vec", "dict" : "Map", "set" : "Set"}
    stype = type(pyobj).__name__
    if len(pyobj) == 0:
        raise AttributeError(f"Contain Empty {stype} and cannot infer the Type. Please give a non empty list or direct use the specific class to define the object.")
    if stype == "list":
        if type(pyobj[0]).__name__ in container_map:
            return [_convert_set(c) for c in pyobj]
        else:
            return pyobj
    elif stype == "dict":
        v0 = list(pyobj.values())[0]
        if type(v0).__name__ in container_map:
            return {c : _convert_set(pyobj[c]) for c in pyobj}
        else:
            return pyobj
    elif stype == "set":
        return list(pyobj)
    else:
        raise AttributeError(f"Not handle {stype}")
        
def frompy(pyobj):
    if type(pyobj) not in [list, set, dict]:
        raise AttributeError("You should give a container within list, set, or dict.")
    class_name = _get_type(pyobj)
    class_obj = getattr(sys.modules[__name__], class_name)
    my_obj = class_obj(_convert_set(pyobj))
    return my_obj

def topy(cstlobj):
    stype = type(cstlobj).__name__
    if stype.startswith("Vec"):
        obj = list(cstlobj)
        if len(obj) > 0 and "cstl" in type(obj[0]).__module__:
            obj = [topy(o) for o in obj]
    elif stype.startswith("Map"):
        obj = dict(cstlobj)
        if len(obj) > 0 and "cstl" in type(list(obj.values())[0]).__module__:
            obj = {o : topy(obj[o]) for o in obj}
    elif stype.startswith("Set"):
        obj = set(cstlobj)
    else:
        raise AttributeError(f"Fail to find the match type for '{cstlobj}' with type {stype}.")
    return obj

"""

open("cstl/cstl.py", "a").write(mywrapper)