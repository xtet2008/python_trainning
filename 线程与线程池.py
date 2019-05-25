# coding:utf-8
# @Time : 2019-05-14 21:19 
# @Author : Andy.Zhang
# @Desc : 线程与线程池
# @Refs : https://www.toutiao.com/i6690398500712088076/

import queue
import threading
import time
from multiprocessing.pool import ThreadPool

if False:
    print('\n' + '-' * 80 + '\n')
    print('''1，使用 threading.Tread()方法创建子（多）线程''')


    def run(name, s):  # 线程要执行的任务
        time.sleep(s)  # 暂停秒数
        print('I am %s' % name)


    # 实例化线程类，并传入函数及其参数
    t1 = threading.Thread(target=run, name='one', args=('One', 5))
    t2 = threading.Thread(target=run, name='two', args=('Two', 2))

    # 开始执行，这两个线程会同步执行
    t1.start()
    t2.start()
    print(t1.getName())  # 获取线程名
    print(t2.getName())


if False:
    print('\n' + '-' * 80 + '\n')
    print('''2，实例Thread类''')


    class MyThread(threading.Thread): # 继承threading中的Thread类
        # 线程所需的参数
        def __init__(self, name, second):
            super().__init__()
            self.name = name
            self.second = second

        # 重写run方法，表示线程所执行的任务，必须有
        def run(self):
            time.sleep(self.second)
            print('I am %s' % self.name)


    # 创建线程实例
    t1 = MyThread('One', 5)
    t2 = MyThread('Two', 2)
    # 启动线程，实际上是调用了类中的run方法
    t1.start()
    t2.start()
    t1.join()  # 阻塞调用程序，直到调用join()方法的线程执行结束，才会继续往下执行
    print(t1.getName())
    print(t2.getName())


if False:
    print('\n' + '-' * 80 + '\n')
    print('''3，setDemon()''')


    def run(name, s):  # 线程要执行的任务
        time.sleep(s)  # 暂停秒数
        print('I am %s' % name)


    # 实例化线程类，并传入函数及其参数
    t1 = threading.Thread(target=run, name='one', args=('One', 5))
    t2 = threading.Thread(target=run, name='two', args=('Two', 2))

    t1.setDaemon(True)  # 给t1设置守护模式，让其随着主线程的结束而结束(不管这个子线程的任务是否完成)

    # 开始执行，这两个线程会同步执行
    t1.start()
    t2.start()  # 主线程会等待未设置守护模式的线程t2执行完成
    print(t1.getName())  # 获取线程名
    print(t2.getName())


if True:
    print('\n' + '-' * 80 + '\n')
    print('''4，多线程互斥锁 threading.Lock(),
    在容易出现抢夺资源的地方进行上锁，实现同一时间内，只有一个线程可以对对象进行操作
    ''')
    a = 0
    print('a=%s, before threading run' % a)
    lock = threading.Lock()  # 实例化互拆锁对象，方便后面的调用

    def incr(n):
        global a
        for i in range(n):
            lock.acquire()  # 上锁的方法
            a += 1  # 在上锁后，解锁前，期间锁住的变量不会被其它线程修改，保证不会多个线程同时修改同一变量，数据不会乱
            lock.release()  # 解锁的方法

    def decr(n):
        global a
        for i in range(n):
            with lock:  # 也可以直接使用with，自动解锁
                a -= 1

    t_incr = threading.Thread(target=incr, args=(1000000, ))
    t_decr = threading.Thread(target=decr, args=(1000000, ))
    t_incr.start()
    t_decr.start()
    t_incr.join()
    t_decr.join()
    print('a=%s, after threading run' % a)

if True:
    print('\n' + '-'*80 + '\n')
    print('''5，队列Queue，
    队列阻塞：程序停在阻塞的位置，无法继续执行''')

    q = queue.Queue(4)  # 实例化队列对象，并设置最大数据量

    print('q.qsize() = %s' % q.qsize())  # 队列长度,返回当前队列数据量(item的个数)
    print('q.empty = %s' % q.empty())  # 判断队列是否为空®

    print("\nq.put 'a', 'b', 'c', 'd'")
    q.put('a')  # 入队，将item 'a'放入队列中，在队列为满时插入值会发生阻塞
    q.put('b')
    q.put('c')
    q.put('d')
    # q.put('e')  # 如果这个代码不注释掉的话，程序会因为队列满了再插入值会发生阻塞（即：此代码后面的所有代码不会被执行，并一直停留在此位置）

    print('\nq.qsize() = %s' % q.qsize())  # 队列长度,返回当前队列数据量(item的个数)
    print('q.full() = %s\n' % q.full())  # 判断队列是否满了

    for i in range(q.qsize()):
        print('q.get() = %s' % q.get())  # 出队，从队列中移除并返回一个数据，在队列为空时获取值会发生阻塞，先进先出，所以取出的是 'a'
        q.task_done()  # 每次get后必须要加 task_done，确认get操作的任务已处理完成，后面的join才取消阻塞。由队列消费者线程调用。
    else:
        pass
        # print(q.get())  # 同椄这个代码如果不取消的话，会因为队列为空获取值发生阻塞

    print('\nq.qsize() = %s' % q.qsize())
    print('q.full() = %s' % q.empty())

    q.join()  # 阻塞挂起调用线程，等待队列中的所有任务被处理掉（队列中所有item全get出队并有执行 task_done），才会执行此代码后面的代码。
    print('done')  # 队列中所有item消费完成后才会执行


if False:
    print('\n' + '-' * 80 + '\n')
    print('''6，自定义线程池：
                    主要是配合队列来进行实现，我们定义好一个队列对象，然后将我们的任务对象put到我们的队列对象中
                    然后使用多线程，让我们的线程去get队列中的对象，然后各自去执行自己get到的任务，
                    这样的话其实实现了线程池
    ''')

    class ThreadPool:  # 自定义线程池
        def __init__(self, n):  # 主线程池
            self.queue_obj = queue.Queue()
            for i in range(n):
                threading.Thread(target=self.worker, daemon=True).start()  # 给于线程worker设置为守护模式（随主线程结束而终止)

        def worker(self):  # 子线程，由于Debug调试的只是主线程中的代码，所以在调试时看不到子线程执行的代码
            """线程对象，写while True是为了能够一直执行任务"""
            while True:  # 让线程执行完一个任务之后不会死掉，主线程结束时，守护模式会让worker的死循环停止
                func = self.queue_obj.get()  # get已经入队的任务，这里会接收到主线程分配的func
                #  由于上面daemon=True，设置了守护模式，当队列为空时，不会一直阻塞在get这里(会随主线程结束而子线程直接杀掉)
                #  有了守护模式，work会在主线程执行完后死后
                func()  # 将队列里的任务拿出来调用
                '''
                这里的func与task_done的顺序非常重要，如果func放在task_done后面的话会出现只执行两次就结束 
                '''
                self.queue_obj.task_done()  # task_done会刷新的计算器
                # 线程池里有一个类似计数器的机制，用来记录put的次数(+1)，每一次task_done都会回拨一次记录的次数(-1)
                # 当回拨完计数器为0之后，就会执行join

        def apply_async(self, func):  # 主线程
            """向队列中传入需要执行的函数对象"""
            self.queue_obj.put(func)  # 将接收的func入队

        def join(self):  # 主线程
            """等待队列中的内容被取完"""
            self.queue_obj.join()  # 队列不为空就阻塞，为空就不阻塞

    # 简单使用
    def task1():  # 子线程
        time.sleep(2)
        print('task1 over')

    def task2():  # 子线程
        time.sleep(3)
        print('task2 over')

    p = ThreadPool(2)  # 如果在 start开启线程之后没有传入任务对象，worker里的get会直接阻塞
    p.apply_async(task1)
    p.apply_async(task2)

    print('threading start')
    p.join()
    print('threading done')

    '''
    如果get发生阻塞意味着队列为空，意味着join不阻塞，意味着print('threading done')会执行
    意味着主线程没有任务在做，意味着主线程结束，意味着不等待设置了守护的线程执行任务，
    意味着子线程会陏主线程的死亡而死亡，这就是为什么设置守护模式
    
    如果没有设置守护模式意味get发生阻塞，意味着子线程任务执行不完，意味着主线程一直要等子线程完成，
    意味着程序一直都结束不了，意味着程序有总是
    '''

if True:
    print('\n' + '-' * 80 + '\n')
    print('''7，Python内置线程池''')
    '''
        原理：
            1. 创建线程池
            2. 将任务扔进云
            3. 关闭线程池
            4. 等待线程任务执行完毕
    '''
    pool = ThreadPool(2)  # 直接使用内置线程池，设置最大线程数

    def task1():
        time.sleep(2)
        print('task1 over')

    def task2(*args, **kwargs):
        time.sleep(3)
        print('task2 over', args, kwargs)

    pool.apply_async(task1)
    pool.apply_async(task2, args=(1, 2), kwds={'a':1, 'b':2})
    print('Task Submitted')
    pool.close()  # 要点：close必须要在join之前，不允许再提交任务了
    pool.join()
    print('Mission Complete')



# End
print('\n' + '-'*80 + '\n')
print('The End')