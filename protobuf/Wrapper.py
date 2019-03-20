from protobuf import FunctionDependentPreprocessing_pb2, FunctionIndependentPreprocessing_pb2

'''
Wrapper for the protobuf classes
'''


def get_triple_by_id(id: int, and_triples: FunctionDependentPreprocessing_pb2.ANDTriples):
    """
    :param id:
    :param and_triples:
    :return: and_triple with the given id or None if it doesn't exist
    """
    for and_triple in and_triples.triples:
        if and_triple.id == id:
            return and_triple
    return None


def get_auth_bit_by_id(id: int, auth_bits: FunctionIndependentPreprocessing_pb2.AuthenticatedBits):
    """
    :param id:
    :param auth_bits:
    :return: auth_bit with given ID or None if ID doesn't exist
    """
    for auth_bit in auth_bits.bits:
        if auth_bit.id == id:
            return auth_bit
    return None
