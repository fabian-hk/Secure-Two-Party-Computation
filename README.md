# Description
This project is a Python implementation of the Two-Party-Computation protocol from the
paper [Authenticated Garbling and Efficient Maliciously Secure Two-Party Computation](https://eprint.iacr.org/2017/030). 
The protocol is based on garbled circuits and our implementation uses the [CBMC-GC-2](https://gitlab.com/securityengineering/CBMC-GC-2) parser to
generate boolean circuits from a C like language. This project was made during a Projekt-INF
at the Universität Stuttgart.

# Installation
To run the program you can use Docker. To install Docker you can do the following:
- For Windows: https://www.docker.com/products/docker-desktop
- For Linux: ```sudo apt-get install docker.io```

To run the program on your computer you need Python version 3.6 or newer and you have to install the following pip packages:
- ```pip install protobuf progress```

# Docker usage 

## Calculated Function
If your preferred function is not available, you have to add the function implemented in C. 
Please see our documentation for further information on which language constructs are available.
It should be named ```functionName.c``` or similar.
The C-file has to be placed in the root of the project.

## Certificates
If you want to use certificates to improve the security, they have to be placed in the corresponding directory
under ```data/certificates*``` 

## On Linux, Mac OS
### Server 
Run server with ```run.sh --server``` with certificates 
or ```run.sh --server -n``` if no certificates should be used.  

### Client
Run client Alice with ```run.sh --alice FUNCTION INPUTS -cn NAME -s SERVER_IP -p SERVER_PORT```.   
Run client Bob with ```run.sh --bob FUNCTION INPUTS -cn NAME -s SERVER_IP -p SERVER_PORT```.   

OR if Server runs on local machine:<br/>
Run client Alice with ```run.sh --alice FUNCTION INPUTS -cn NAME ```.   
Run client Bob with ```run.sh --bob FUNCTION INPUTS -cn NAME```.   

OR if no certificates needed:<br/>
Run client Alice with ```run.sh --alice FUNCTION INPUTS -n```.   
Run client Bob with ```run.sh --bob FUNCTION INPUTS -n```.  

## Windows

The server can't be used under Windows because it uses several processes and they have
to pass socket object to each other. So you have to use Docker for the server. We recommend
to use Docker also for the clients for optimal stability.

# Usage with command line

## Setup
1. You have to compile the [CBMC-GC-2](https://gitlab.com/securityengineering/CBMC-GC-2) parser for your system and 
put the ```cbmc-gc``` executable in the ```data/CBMC-GC-2/bin``` folder.
2. Make it executable: ```chmod +x cbmc-gc```
3. If you want to use your own certificate you can create them and sign them with the
root-ca private key in the ``data/certificates/`` folder and then you have to copy the 
signed certificate in the same folder. After this you can either specify the certificate
at runtime with ``-c`` or configure it in the ``conf/cert_conf.py`` file. For information
on how to create certificates read the section ``Create certificates``. However there 
are already signed certificates for alice and bob so you can use them if you just want to 
test the program.

## Run
1. Run the server: ```python3 Server.py``` => with TLS encryption
2. Run Alice: ```python3 TwoPartyComputation.py add 4 -c certficiate-alice -cn bob.mpc```
3. Run Bob: ```python3 TwoPartyComputation.py add 5 -c certificate-bob -cn alice.mpc```

Here are all available options listed:
````bash
usage: TwoPartyComputation.py [-h] [-cn CN] [-c CERTIFICATE] [-n] [-s SERVER]
                              [-p PORT]
                              circuit input [input ...]

Script for maliciously secure Two-Party Computation. You should start the script from the directory of this repository.

positional arguments:
  circuit               Either one of the example circuits or a path to an
                        parsable c-code file (ending .c). Path must be relativ
                        to the location of this file.
  input                 Own input to the circuit as an Integer.

optional arguments:
  -h, --help            show this help message and exit
  -cn CN                Common name of the partner you want to talk to.
  -c CERTIFICATE, --certificate CERTIFICATE
                        Own certificate to authenticate your self to the other
                        party (should be specified in the conf.py file).
  -n, --noencryption    Specify this option if you don't care about security
                        and want to use unencrypted communication
  -s SERVER, --server SERVER
                        IP address for the server which provides Fpre and the
                        communication between the clients.
  -p PORT, --port PORT  The port of the server specified by -s (default 8448).

Example usage:
        python3 TwoPartyComputation.py add 45 -cn bob.mpc -s 10.10.1.42 -p 4444
        python3 TwoPartyComputation.py cbmc_parser/ansi_c_code/addition.c 52 -cn bob.mpc -s 10.10.1.42 -p 4444

````

# Information about the gate IDs
The gate IDs must always end with a zero so that the gate wires can have 
unique IDs. The input A has the id xxx0 the input B has the id xxx1 and
the output Y has the id xxx2

# Create certificates
- [Tutorial](https://legacy.thomas-leister.de/eine-eigene-openssl-ca-erstellen-und-zertifikate-ausstellen/) how to generate certificates
- Certificates should always have the ending ``-pub.pem``
- Private keys should always end on ``-key.pem``

# Contributors
- Fabian Hauck
- Marcel Galuschka
- Simon Bihlmaier
- Julian Obst
