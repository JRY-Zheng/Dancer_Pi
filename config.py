_configs = {
    # 配置数据库',
    'server': 'server',
    'catalog': 'catalog',
    'user': 'user',
    'password': 'password',
    'port': 'port',
    # 程序信息
    'version': 'v 0.0.1',
    # 配置音乐存放目录',
    'dir': '~/Music',
    'ignore': []
}

try:
    import config_override
    _configs = dict(_configs, **config_override.configs)
except ImportError:
    pass


class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D

configs = toDict(_configs)
