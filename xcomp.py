from itertools import product
from contextlib import contextmanager


def comp(collector):
    def decorator(func):
        return collector(func())
    return decorator


def multi_comp(*collectors):
    def decorator(func):
        return tuple(c(v) for c, v in zip(collectors, zip(*func())))
    return decorator


class BreakReduce(Exception):
    pass


class ContinueReduce(Exception):
    pass


@contextmanager
def ignore(exception):
    try:
        yield
    except exception:
        pass


def multi_reduce_comp(*inits, iters=(), iter_=None,
                      result=lambda *args: args):
    if iter_ is not None:
        iters = (iter_,)

    def decorator(func):
        accums = inits
        with ignore(BreakReduce):
            for vs in product(*iters):
                with ignore(ContinueReduce):
                    accums = func(*accums, *vs)
        return result(*accums)
    return decorator


def reduce_comp(init, iters=(), iter_=None,
                result=lambda *args: args):
    def decorator(func):
        def multi(*args):
            return func(*args),
        return multi_reduce_comp(init, iters=iters,
                                 iter_=iter_, result=result)(multi)[0]
    return decorator


def delay_arg(func, *args, **kwargs):
    def delayed(arg):
        return func(arg, *args, **kwargs)
    return delayed
