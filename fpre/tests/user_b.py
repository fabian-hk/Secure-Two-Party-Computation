from fpre.fpre import Fpre
import fpre.f_la_and as flaand
from protobuf import FunctionDependentPreprocessing_pb2
import conf

certificate = "certificate-bob"
partner = "alice.mpc"

com = Fpre(conf.test_server_ip, conf.test_server_port, certificate, partner)
com.init_fpre()

auth_bits = flaand.get_authbits(com.person, com, 2)
and_triple = FunctionDependentPreprocessing_pb2.ANDTriple()
and_triple.id = 0
auth_bits = iter(auth_bits.bits)
auth_bit = next(auth_bits)
and_triple.r1 = auth_bit.r
and_triple.M1 = auth_bit.M
and_triple.K1 = auth_bit.K
auth_bit = next(auth_bits)
and_triple.r2 = auth_bit.r
and_triple.M2 = auth_bit.M
and_triple.K2 = auth_bit.K

flaand.f_la_and(com, com.person, and_triple)

com.close_session()
