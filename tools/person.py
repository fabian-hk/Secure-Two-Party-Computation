import os

import conf


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
        # Whereby the wire for the MSB is the first element and the wire for de LSB is
        # the last element.
        self.other_inputs = []

        self.in_vals = {}

        if self.x == Person.A:
            self.delta = os.urandom(int(conf.k / 8))

    def __str__(self):
        return "Person: " + str(self.x) + " Delta: " + str(self.delta)

    def load_input_string(self, in_val: str):
        for ids, bit in zip(self.inputs, in_val):
            for id in ids:
                self.in_vals[id] = int(bit).to_bytes(1, byteorder='big')

    def load_input_integer(self, in_val: int):
        n = in_val
        for ids in reversed(self.inputs):
            if n > 0:
                for id in ids:
                    self.in_vals[id] = int(n & 1).to_bytes(1, byteorder='big')
                n = n >> 1
            else:
                for id in ids:
                    self.in_vals[id] = b'\x00'
