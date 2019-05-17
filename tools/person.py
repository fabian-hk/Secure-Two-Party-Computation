import os
from typing import List

from conf import conf


class Person:
    A = 0
    B = 1

    def __init__(self, x):
        """
        :param x:
        """
        self.x = x
        self.delta = None

        # List to store all input wire IDs for this person.
        # Whereby the wire for the MSB is the first element and the wire for de LSB is
        # the last element.
        self.inputs = []

        # List to store all input wire IDs for the other person.
        # Whereby the wire for the LSB is the first element and the wire for de MSB is
        # the last element.
        self.other_inputs = []

        self.in_vals = {}

        if self.x == Person.A:
            self.delta = os.urandom(int(conf.k / 8))

    def __str__(self):
        return "Person: " + str(self.x) + " Delta: " + str(self.delta)

    def load_input_string(self, in_vals: List[str]):
        if len(in_vals) != len(self.inputs):
            raise IndexError()

        i = 0
        for in_val in in_vals:
            for ids, bit in zip(self.inputs[i], in_val):
                for id in ids:
                    self.in_vals[id] = int(bit).to_bytes(1, byteorder='big')
            i += 1

    def load_input_integer(self, in_vals: List[int]):
        if len(in_vals) != len(self.inputs):
            raise IndexError()

        i = 0
        for in_val in in_vals:
            n = in_val
            for ids in reversed(self.inputs[i]):
                if n != 0:
                    for id in ids:
                        self.in_vals[id] = int(n & 1).to_bytes(1, byteorder='big')
                    n = n >> 1
                else:
                    for id in ids:
                        self.in_vals[id] = b'\x00'
            i += 1
