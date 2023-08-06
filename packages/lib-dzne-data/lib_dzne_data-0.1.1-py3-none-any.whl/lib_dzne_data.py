 
import string
import pandas as pd
from collections import defaultdict
import Bio.Seq

def copy(data, allow_None=False):
    if allow_None and (data is None):
        return float('nan')
    if type(data) in {float, int, str, bool}:
        return data
    if type(data) is Bio.Seq.Seq:
        raise TypeError("Bio.Seq.Seq has to be converted to str! ")
    errors = list()
    try:
        data = dict(data)
    except Exception as e:
        errors.append(e)
    else:
        keys = list(data.keys())
        for k in keys:
            data[k] = copy(data[k], allow_None=allow_None)
        return data
    try:
        data = list(data)
    except Exception as e:
        errors.append(e)
    else:
        for i in range(len(data)):
            data[i] = copy(data[i], allow_None=allow_None)
        return data
    raise ExceptionGroup(errors)



def isna(*values):
    ans, = {pd.isna(x) for x in values}
    return ans

def notna(*values):
    ans, = {pd.notna(x) for x in values}
    return ans

def allisna(*values):
    return all(pd.isna(x) for x in values)

def allnotna(*values):
    return all(pd.notna(x) for x in values)

def anyisna(*values):
    return any(pd.isna(x) for x in values)

def anynotna(*values):
    return any(pd.notna(x) for x in values)




def strkeyallowed(key):
    if type(key) is not str:
        return False
    if len(set(key) - set(string.ascii_lowercase + string.digits + '-')):
        return False
    return True



def parse_key(key):
    parts = key.split('.')
    ans = list()
    for part in parts:
        if len(set(part) - set(string.digits)):
            if strkeyallowed(part):
                ans.append(part)
            else:
                raise ValueError()
        else:
            ans.append(int(part))
    return tuple(ans)


def flatten(data):
    if type(data) in (str, int, float, bool):
        return data
    pile = {None:data}
    ans = {}
    while len(pile):
        oldkey, oldvalue = pile.popitem()
        if type(oldvalue) in {str, int, float, bool}:
            if oldkey in ans.keys():
                raise KeyError()
            if oldkey is None:
                raise ValueError()
            ans[oldkey] = oldvalue
            continue
        if type(oldvalue) is list:
            iterator = enumerate(oldvalue)
        elif type(oldvalue) in (dict, defaultdict):
            iterator = oldvalue.items()
        else:
            raise TypeError(f"The value {oldvalue.__repr__()} is of the invalid type {type(oldvalue)}! ")
        for k, v in iterator:
            if oldkey is None:
                newkey = ""
            else:
                newkey = oldkey + '.'
            if type(oldvalue) is list:
                newkey += str(k)
            elif strkeyallowed(k):
                newkey += k
            else:
                raise KeyError(f"{k.__repr__()} is not a valid key! ")
            if newkey in pile.keys():
                raise KeyError()
            pile[newkey] = v
    return ans


def extract_from_dict(dictionary, *, keys, demand=False):
    ans = dict()
    for k in keys:
        if (k not in dictionary.keys()) and (not demand):
            continue
        ans[k] = dictionary.pop(k)
    return ans


