import os
import conf


def init():
    return os.urandom(int(conf.k / 8))


def create_gate_vars():
    # TODO compute correct keys and tags
    return os.urandom(int(conf.k / 8)), os.urandom(int(conf.k / 8))
