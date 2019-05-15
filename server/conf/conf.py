k = 128
input_size = 320  # number of input bits
upper_bound_gates = 11000

# path to the cbmc compiler
cbmc_path = "../../../data/CBMC-GC-2/bin/"
default_output = "cbmc_parser/gate_files/default_output/"

# on Windows it has to be the address of the "Hyper-V Virtual Ethernet Adapter #2" if you use docker
test_server_ip = '10.0.75.2'
test_server_port = 8448
