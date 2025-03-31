from decimal import Decimal


class frange:

    def __init__(self, start=0, stop=None, step=1):

        if stop is None:
            stop = start
            start = 0

        self.__start = self.validator(start)
        self.__stop = self.validator(stop)
        self.__step = self.validator(step)
        self.__index = self.__start

    @classmethod
    def validator(cls, value):
        if not isinstance(value, (float, Decimal, int)):
            raise TypeError('Value must be numeric')
        return Decimal(value)

    def __iter__(self):
        return self

    def __next__(self):
        if (self.__step > 0 and self.__index >= self.__stop) or (self.__step < 0 and self.__index <= self.__stop):
            raise StopIteration
        cur = self.__index
        self.__index += self.__step
        return cur


    def print_fr(self):
        return self.__start, self.__stop, self.__step
