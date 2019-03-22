from protobuf import FunctionDependentPreprocessing_pb2

'''
Wrapper for the FunctionDependentPreprocessing_pb2 file
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
