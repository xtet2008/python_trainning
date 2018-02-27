#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/5 15:05
# @Author  : ZhangSheng@xiaoyezi.com
# @File    : pattern_state.py

__author__ = 'kevinlu1010@qq.com'

from abc import ABCMeta, abstractmethod


class State():
    __metaclass__ = ABCMeta

    @abstractmethod
    def write_code(self):
        pass


class Morning(State):
    def write_code(self, work):
        if work.hour <= 12 and work.hour > 8:
            print '上午工作，精神百倍'
        else:

            work.set_status(Noon())
            work.write_code(work)


class Noon(State):
    def write_code(self, work):
        if work.hour <= 14 and work.hour>12 :
            print '中午工作，困，想午休'
        else:
            work.set_status(Afternoon())
            work.write_code(work)


class Afternoon(State):
    def write_code(self, work):
        if work.hour <= 18 and work.hour>14:
            print '下午工作，状态不错'
        else:
            work.set_status(Eve())
            work.write_code(work)


class Eve(State):
    def write_code(self, work):
        if work.hour <= 22 and work.hour>18:
            print '加班了，状态不太好'
        else:
            work.set_status(Night())
            work.write_code(work)


class Night(State):
    def write_code(self, work):
        if work.hour <= 8 or work.hour > 22:
            print '不行了，要睡觉了'
        else:
            work.set_status(Morning())
            work.write_code(work)


class Work():
    def __init__(self, hour):
        self.hour = hour
        self.state = Morning()

    def set_status(self, state):
        self.state = state

    def write_code(self, work):
        self.state.write_code(work)


if __name__ == '__main__':
    work = Work(10)
    for hour in (3, 11, 12, 13, 14, 17, 19, 22, 23,12):
        work.hour = hour
        print '%d点，' % hour
        work.write_code(work)