from tools import fpre
import conf
import os

class Person:
    A = 0
    B = 1

    def __init__(self, x):
        """
        :param x:
        """
        self.x = x
        self.delta = None

        #personal key delta
        self.delta = os.urandom(int(conf.k/8))

    def __str__(self):
        return "Person: "+str(self.x)+" Delta: "+str(self.delta)
