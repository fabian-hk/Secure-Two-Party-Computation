k = 128
input_size = 8  # number of input bits
upper_bound_gates = 1500

test_server_ip = 'localhost'
test_server_port = 8448

crt_storage = '/docker/certificates/'
root_cert = crt_storage + 'ca-root.pem'
# certificate if you run the program as user
certificate = crt_storage + 'certificate-bob-pub.pem'
priv_key = crt_storage + 'certificate-bob-key.pem'
# certificate if you run the program as server
#server_certificate = crt_storage + 'certificate-localhost-pub.pem'
#server_priv_key = crt_storage + 'certificate-localhost-key.pem'

# path to the cbmc compiler
cbmc_path = "../../../docker/cbmc/"
default_output = "cbmc_parser/gate_files/default_output"
