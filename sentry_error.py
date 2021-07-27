# import sentry_sdk

# sentry_sdk.init("http://7f91324a028548e584f2eeef95bd7ec4@10.150.27.209:9000/8")
#
# division_by_zero = 1 / 0
#
# if False:
#     # from geoip import geolite2
#     # import geoip
#     # geoip2 = geoip.geolite2
#     import geoip2.database
#     #reader = geoip2.database.Reader('~/GeoLite2/GeoLite2-City.mmdb')
#     reader = geoip2.database.Reader('/Users/BEJ-NB-2077/GeoLite2/GeoLite2-City.mmdb')
#
#     # response = reader.city('128.101.101.101')
#     # response = reader.city('219.142.140.226')
#     response = reader.city('175.4.79.187')
#
#     print(response)
#     print(response.country.name)
#     print(response.country.names['zh-CN'])
#     print(response.traits.network)
#
#     #line = geolite2.lookup('219.142.140.226'.encode('utf-8'))
#
#     reader.close()
#
#
#
#
# from multiprocessing import Process
# import os
#
# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())
#
# def f(name):
#     info('function f')
#     print('hello', name)
#
# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()


class Node:
    data = None
    next = None


def create_link_list(node_arr):
    head_node = None
    next_node = None
    for i in node_arr:
        node = Node()
        node.data = i
        node.next = None
        if head_node is None:
            head_node = node
            next_node = head_node
        else:
            next_node.next = node
            next_node = node

    return head_node


def print_link_list(head):
    _list = []
    while head is not None:
        # print(head.data)
        _list.append(head.data)
        head = head.next
    print(_list)


def reverse1(head):
    if head is None or head.next is None:
        return head
    current = head
    pre = None
    pnext = None
    while current is not None:
        pnext = current.next
        current.next = pre
        pre = current
        current = pnext

    return pre


def reverse2(current):
    if current.next is None:
        return current
    pnext = current.next
    current.next = None
    reversed = reverse2(pnext)
    pnext.next = current

    return reversed


def reverse3(current, pre):
    if current.next is None:
        current.next = pre
        return current
    else:
        pnext = current.next
        current.next = pre
        return reverse3(pnext, current)


if __name__ == '__main__':
    head = create_link_list([1, 2, 3, 4, 5])
    print_link_list(head)  # 输出，[1,2,3,4,5, ...]

    # 求写一段代码(例如以下示例代码)实现将以上 head 反转，并且最终输出结果如下
    def reverse_link(head):
        pass

    new_head = reverse_link(head)
    print_link_list(new_head)  # 输出 [5, 4, 3, 2, 1]





    # import copy
    #
    # l1 = [1, 2, [3, 4]]
    # l2 = copy.copy(l1)
    # l1.append(5)
    # l1[2].append(5)  # 子对象 改变
    # print(l1)
    # print(l2)
    # [1, 2, [3, 4, 5], 5]
    # [1, 2, [3, 4, 5]]


    class Obj:
        def __init__(self):
            pass

        def __new__(cls, *args, **kwargs):
            if not hasattr(Obj, "_instance"):  # 反射
                Obj._instance = object.__new__(cls)
            return Obj._instance

    obj1 = Obj()
    obj2 = Obj()

    print(obj1 is obj2)  # 要求输出结果为 True

    import copy

    a = ['a', 'b', 'c', [0, 1, 2], 'd']
    b = a
    c = copy.copy(a)
    d = copy.deepcopy(a)

    a.append('e')
    a[3].append(3)

    print(a)
    print(b)
    print(c)
    print(d)



    def fn(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10):
        print(arg1)
        print(arg2)
        print(arg3)
        print(arg4)
        print(arg5)
        print(arg6)
        print(arg7)
        print(arg8)
        print(arg9)
        print(arg10)

    fn(1, 2, 3, 4, a=1, b=2,)