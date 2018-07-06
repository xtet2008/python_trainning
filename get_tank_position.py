# -*- coding: UTF-8 -*-
# Write by Andy.Zhang
# Email: xtet2008@126
# WeChat: 186 1845 8391
# Datetime: 2018/7/6 15:58:37

import unittest


class Switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


class Tank:
    position = {
        'WL': 'S',  # 西左 => 南
        'WR': 'N',  # 西右 => 北
        'EL': 'N',  # 东左 => 北
        'ER': 'S',  # 东右 => 南
        'NL': 'W',  # 北左 => 西
        'NR': 'E',  # 北右 => 东
        'SL': 'E',  # 南左 => 东
        'SR': 'W'   # 南右 => 西
    }

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def get_position(self, string):
        for s in string:
            if s == 'M':  # 如果坦克开了100米后，则根据方向修正x或y的值
                for case in Switch(self.direction):
                    if case('W'):  # 向W西移动100米，x-1
                        self.x -= 1
                        break
                    if case('E'):  # 向E东移动100米，x-1
                        self.x += 1
                        break
                    if case('N'):  # 向北移动100米，y+1
                        self.y += 1
                        break
                    if case('S'):  # 向南移动100米，y-1
                        self.y -= 1
                        break
                    if case():  # 忽略其他参数
                        print ('ignore the args: %s' % self.direction)
                        break

            elif s in ['L', 'R']:  # 如果坦克向左/右拐弯了，则根据当前方位+左/右拐向重新校正方位
                self.direction = self.position[self.direction+s]
        else:
            return self.x, self.y, self.direction


class TankTestCase(unittest.TestCase):
    """测试坦克移动信号"""

    def setUp(self):
        self.message = 'MTMPRPMTMLMRPRMTPLMMTLMRRMP'
        self.new_tank = Tank(11, 39, 'W')

    def tearDown(self):
        self.message, self.new_tank = None, None

    def testTankMessage(self):
        """根据输入参数 'MTMPRPMTMLMRPRMTPLMMTLMRRMP' 能否正确输出   """
        self.assertEqual(self.new_tank.get_position(self.message), (9, 43, 'E'))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TankTestCase('testTankMessage'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')