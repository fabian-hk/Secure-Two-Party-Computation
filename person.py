from random import randint
import conf
import math


class Person:
    A = 0
    B = 1

    def __init__(self, x):
        self.x = x
        self.delta = randint(0, math.pow(2, conf.k))
