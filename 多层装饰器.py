# -*- coding: utf-8 -*-


def first(func):
    print '%s() was post to first()' % func.func_name

    def _first(*args, **kw):
        print 'Call the function %s() in _fist().' % func.func_name
        return func(*args, **kw)
    return _first


def second(func):
    print '%s() was post to second()' % func.func_name

    def _second(*args, **kw):
        print 'Call the function %s() in _second.' % func.func_name
        return func(*args, **kw)
    return _second


@first
@second
def test():
    print 'hello world'

if __name__ == '__main__':
    test()
