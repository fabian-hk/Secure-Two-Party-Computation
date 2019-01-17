from random import randint
import conf
import math
import os


class Person:
    A = 0
    B = 1

    def __init__(self, x):
        """
        :param x:
        """
        self.x = x
        self.delta = os.urandom(int(conf.k/8))
