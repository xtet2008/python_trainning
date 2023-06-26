# -*- coding: utf-8 -*-

# This coding should be running in Python3
from multiprocessing import Process
from threading import Thread
import os, time, sys


class TestCompute(object):
    def __init__(self):
        if sys.version_info[0] > 2:  # Python3 else Python2
            print('\ncpu count: %s' % os.cpu_count())  # cpu为几核

    def work(self):
        res = 0
        for i in range(100000000):
            res *= i

    def run(self, tag='Process'):
        l = []
        start = time.time()
        for i in range(os.cpu_count() if sys.version_info[0] > 2 else 4):
            p = Process(target=self.work) if tag == 'Process' else Thread(target=self.work) # 耗时x秒
            l.append(p)
            p.start()

        for p in l:
            p.join()

        stop = time.time()
        print('计算密集型任务,', 'Process多进程时间统计：' if tag == 'Process' else 'Thread多线程时间统计：', stop-start)


class TestIO(object):
    def __init__(self):
        if sys.version_info[0] > 2:  # Python3 else Python2
            print('\ncpu count: %s' % os.cpu_count())  # cpu为几核

    def work(self):
        time.sleep(2)

    def run(self, tag='Process'):
        l = []
        start = time.time()
        for i in range(4000):
            p = Process(target=self.work) if tag == 'Process' else Thread(target=self.work)
            # 这种io密集型任务如果用多进程的话，大部分时间会耗在创建进程上
            l.append(p)
            p.start()

        for p in l:
            p.join()

        stop = time.time()
        print('I/O等待密集型任务,', 'Process多进程时间统计：' if tag == 'Process' else 'Thread多线程时间统计：', stop - start)


if __name__ == '__main__':
    test1 = TestCompute()
    # print ('process test starting')
    test1.run(tag='Process')
    # print ('Thread test starting')
    test1.run(tag='Thread')
    print('测试结论：并发多个计算密集型任务，多进程效率高')

    test2 = TestIO()
    # print ('process test starting')
    test2.run(tag='Process')
    # print ('Thread test starting')
    test2.run(tag='Thread')
    print('测试结论：并发多个I/O密集型任务，多线程效率高')


