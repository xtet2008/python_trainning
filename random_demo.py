# coding: utf-8
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/20 19:02
# @Author  : ZhangSheng@xiaoyezi.com
# @File    : random_demo.py

import random


def random_index(rate):
    """随机变量的概率函数"""
    #
    # 参数rate为list<int>
    #
    start = 0
    randnum = random.randint(1, sum(rate))

    for index, item in enumerate(rate):
        print 'index, item = ', index, item
        start += item
        if randnum <= start:
            break
    return index


def main():
    arr = ['red', 'green', 'blue']
    rate = [30, 45, 25]

    red_times = 0
    green_times = 0
    blue_times = 0
    others = 0
    for i in xrange(10000):
        random.seed()
        random_color = arr[random_index(rate)]

        if random_color == 'red':
            red_times += 1
        elif random_color == 'green':
            green_times += 1
        elif random_color == 'blue':
            blue_times += 1
        else:
            others += 1
            # print 'others'

    print red_times, green_times, blue_times, others


def get_random_option_by_rate(option_rate=[1, 1]):
    if not option_rate or not sum(option_rate) or sum([abs(int(i)) for i in option_rate]) != sum(option_rate):
        return 0

    random.seed()
    rand_val = random.randint(1, sum(option_rate))
    item_sum = 0
    for index, item in enumerate(option_rate):
        item_sum += item
        if rand_val <= item_sum:
            break

    return index+1

def test_random():
    _true, _false = 0, 0
    for i in xrange(1000):
        _value = get_random_option_by_rate(option_rate=[1, 1])
        if _value:
            if _value == 1:
                _true += 1
            else:
                _false += 1
        else:
            pass
    print '_true, _false = ', _true, _false


if __name__ == '__main__':
    # main()
    test_random()