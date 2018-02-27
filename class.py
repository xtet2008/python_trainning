# -*- coding: utf-8 -*-


class Test(object):
    def __init__(self):
        second = 'I will created after the one'
    one = 'I will created before the second'

    def instancefun(self):  # 实例方法
        print('instancefun')
        print(self)

    @classmethod  # 类方法
    def classfun(cls):
        print('classfun')
        print(cls)

    @staticmethod  # 静态方法
    def staticfun():
        print('staticfun')

    def function():  # 普通函数
        print('func')


obj_t = Test()
# obj_t.instancefun
obj_t.instancefun()  # 对象调用实例方法
# obj_t.function  # 对象不能调用函数？
obj_t.staticfun()  # 静态方法
obj_t.classfun()  # 类方法
print '---------------------------------------'
Test.instancefun(obj_t)
# Test.instancefun(Test)
# Test.function()
Test.staticfun()
Test.classfun()
