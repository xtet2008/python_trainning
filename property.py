
# -*- coding: utf-8 -*-

from decimal import Decimal

########################################################################


class Fees(object):
    '''just for test''' # docment
    """"""
    def __init__(self):
        """Constructor"""
        self._fee = None

    @property
    def fee(self):
        """
        The fee property - the getter
        """
        return self._fee

    @fee.setter
    def fee(self, value):
        """
        The setter of the fee property
        """
        if isinstance(value, str):
            self._fee = Decimal(value)
        elif isinstance(value, Decimal):
            self._fee = value

    @fee.deleter
    def fee(self, attr_name):
        if self.__getattribute__(attr_name):
            self.__delattr__(attr_name)



if __name__ == "__main__":
    f = Fees()
    f.fee = '1'  # setter()
    print f.fee  # getter()
    print f.delete('_fee')  # delete()  # question: why error?
    print f.fee
