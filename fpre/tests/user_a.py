from fpre.fpre import Fpre
from fpre.f_a_and import f_a_and
import conf

certificate = "certificate-alice"
partner = "bob.mpc"

com = Fpre(conf.test_server_ip, conf.test_server_port, certificate, partner)
com.init_fpre()
and_triples = f_a_and(com.person, com, 20)
com.close_session()
