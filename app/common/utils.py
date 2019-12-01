# -*- coding: utf-8 -*-
import time


def callback(f):
    def wrapper(obj, *args, **kwargs):
        resp = f(obj, *args, **kwargs)
        if kwargs.get('callback'):
            mcallback = kwargs['callback']
            func = None
            if isinstance(callback, str) and hasattr(obj, mcallback):
                func = getattr(obj, mcallback)
            elif hasattr(mcallback, 'im_self') and mcallback.im_self is obj:
                func = mcallback
                kwargs['callback'] = func.__name__
            else:
                raise NotImplementedError("self.%s() not implemented!" % callback)

            if func is None:
                return resp
            else:
                return func(resp)
        else:
            return resp
    return wrapper


def time_consumed(f):
    def wrapper(obj, *args, **kwargs):
        time0 = time.time()
        res = f(obj, *args, **kwargs)
        print(f.__name__ + ' consumed time %.3f seconds !\n' % time.time()-time0)
        return res
    return wrapper


def WorkFlow(f):
    def wrapper(ParentModuel, SonModuel, Function, *args, **kwargs):
        pass


if __name__ == '__main__':
    pass
