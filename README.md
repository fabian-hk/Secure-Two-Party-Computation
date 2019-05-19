# Description
This project is a Python implementation of the maliciously secure Two-Party-Computation protocol from the
paper [Authenticated Garbling and Efficient Maliciously Secure Two-Party Computation](https://eprint.iacr.org/2017/030). 
The protocol is based on garbled circuits and our implementation uses the [CBMC-GC-2](https://gitlab.com/securityengineering/CBMC-GC-2) parser to
generate boolean circuits from a C like language. This project was made during a Projekt-INF
at the Universität Stuttgart.

# Installation
To run the program you can use Docker. To install Docker you can do the following:
- For Windows: https://www.docker.com/products/docker-desktop
- For Linux: ```sudo apt-get install docker.io```

To run the program on your computer you need Python version 3.6 or newer and you have to install the following pip packages:
- ```pip3 install protobuf progress```

# Setup
1. You have to compile the [CBMC-GC-2](https://gitlab.com/securityengineering/CBMC-GC-2) parser for your system and 
put the ```cbmc-gc``` executable in the ```data/CBMC-GC-2/bin``` folder.
2. Make it executable: ```chmod +x cbmc-gc```
3. If you want to use your own certificates, you can create and sign them with the
root-ca private key in the ``data/certificates/`` folder and then you have to copy the 
signed certificates in the same folder. After that you can either specify the certificates
at runtime with ``-c`` or configure them in the ``conf/cert_conf.py`` file. For information
on how to create certificates read the section ``Create certificates``. However there 
are already signed certificates for alice and bob, so you can use them if you just want to 
test the program.

# Usage with Docker 

## Calculated Function
If your preferred function is not available, you have to add the function implemented in C. 
For further information look at the website of the CBMC-GC-2 parser on which language constructs are available.
It should be named ```functionName.c``` or similar.
The C-file has to be placed in the root of the project.

## Certificates
If you want to use certificates to improve the security, they have to be placed in the corresponding directory
under ```data/certificates*``` 

## On Linux, Mac OS
### Server 
Run server with ```./run.sh --server``` when you use certificates 
and with ```./run.sh --server -n``` if no certificates shall be used.  

### Client
Run client Alice with ```./run.sh --alice FUNCTION INPUTS -cn NAME -s SERVER_IP -p SERVER_PORT```.
Run client Bob with ```./run.sh --bob FUNCTION INPUTS -cn NAME -s SERVER_IP -p SERVER_PORT```.   

If server runs on your local machine:<br/>
Run client Alice with ```./run.sh --alice FUNCTION INPUTS -cn NAME ```.
Run client Bob with ```./run.sh --bob FUNCTION INPUTS -cn NAME```.   

If no certificates are used:<br/>
Run client Alice with ```./run.sh --alice FUNCTION INPUTS -n```.
Run client Bob with ```./run.sh --bob FUNCTION INPUTS -n```.  

## Windows

The server can't be used under Windows, because it uses several processes which have
to pass socket objects to each other. So you have to use Docker for the server. For optimal stability 
we recommend to use Docker also for the clients. You can use the ```run.bat``` script
exactly like the run.sh script for Linux and Mac OS.

# Usage with command line

1. Run the server: ```python3 Server.py``` => with TLS encryption
2. Run Alice: ```python3 TwoPartyComputation.py add 4 -c certficiate-alice -cn bob.mpc```
3. Run Bob: ```python3 TwoPartyComputation.py add 5 -c certificate-bob -cn alice.mpc```

Here are all the available options listed:
````
usage: TwoPartyComputation.py [-h] [-cn CN] [-c CERTIFICATE] [-n] [-s SERVER]
                              [-p PORT]
                              circuit input [input ...]

Script for maliciously secure Two-Party Computation. You should start the script from the directory of this repository.

positional arguments:
  circuit               either one of the example circuits or a path to an
                        parsable c-code file (ending .c); path must be relativ
                        to the location of this file
  input                 own input to the circuit as integers

optional arguments:
  -h, --help            show this help message and exit
  -cn CN                common name of the partner you want to talk to
  -c CERTIFICATE, --certificate CERTIFICATE
                        own certificate to authenticate yourself to the other
                        party (should be specified in the cert_conf.py file)
  -n, --noencryption    specify this option if you don't care about security
                        and if you want to use unencrypted communication
  -s SERVER, --server SERVER
                        IP address for the server which provides Fpre and the
                        communication between the clients (default localhost)
  -p PORT, --port PORT  the port of the server specified by -s (default 8448)

Example usage:
        python3 TwoPartyComputation.py add 45 -cn bob.mpc -s 10.10.1.42 -p 4444
        python3 TwoPartyComputation.py cbmc_parser/ansi_c_code/addition.c 52 -cn bob.mpc -s 10.10.1.42 -p 4444

````

# Usage as API in your own project

If you want to use this project as a Python module in you own project, you have
to create an Fpre object for the communication and a MPC object for the actual
MPC protocol. The following code shows how to connect to the server (which you have
to start separately), how to load the input and a function written in C and finally
how to execute the MPC protocol and how to determine the output as an integer.

````python
from tools.person import Person
import tools.helper as h
from MPC import MPC
from fpre.fpre import Fpre
import cbmc_parser.create_circuit as cc

# Initialize connection and determine who is A and who is B
com = Fpre("10.10.5.143", 8448, "certificate-bob", "alice.mpc", False)

# Initialize MCP class which will do the garbling and evaluation
mpc = MPC(com)

# First do the function independent preprocessing to generate authenticated bits
mpc.function_independent_preprocessing()

# Parse the circuit and load the inputs for the person
inputs, outputs, num_and, gatelist = cc.create_circuit("path_to/program.c", com.person)
try:
    com.person.load_input_integer([34, 12])
except IndexError:
    com.close_session()
    raise IndexError()
mpc.load_cirucit(inputs, outputs, num_and, gatelist)

# Do the function dependent preprocessing which garbles the circuit
mpc.function_dependent_preprocessing()

# Create masked input bits
mpc.input_processing()

# Person B evaluates the circuit
if com.person.x == Person.B:
    mpc.circuit_evaluation()

# Determine the real output values
result = mpc.output_determination()

# Print the output as binary and decimal number to the console
h.print_output(result)
````

# Information about the gate IDs
The gate IDs must always end with a zero so that the gate wires can have 
unique IDs. The input A has the id xxx0, the input B has the id xxx1 and
the output Y has the id xxx2.

# Create certificates
- [Tutorial](https://legacy.thomas-leister.de/eine-eigene-openssl-ca-erstellen-und-zertifikate-ausstellen/) how to generate certificates
- Certificates should always have the ending ``-pub.pem``
- Private keys should always end on ``-key.pem``

# Contributors
- Fabian Hauck [GitHub](https://github.com/fabian-hk)
- Marcel Galuschka
- Simon Bihlmaier
- Julian Obst
