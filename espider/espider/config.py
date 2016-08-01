#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    espider.conf.config.py
    ------------------------------------------------------------------

    config file used for espider

"""

from espider import config_default

configs = config_default.configs

class Dict(dict):
    """
        A dict that support x.y style
    """
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k,v in zip(names, values):
            self[k] = v

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError("'Dict' object has no attribute '%s'" %item)

    def __setattr__(self, key, value):
        self[key] = value

def toDict(d):
    D = Dict()
    for k,v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D


def merge(default, override):
    """

    :rtype: dict
    """
    r = {}
    for k,v in default.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v ,override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    print('cannot import specific configs, espider will use default configs')

configs = toDict(configs)

if __name__ == '__main__':
    print(configs)