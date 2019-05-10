# Installation
Dependencies:
- ```Docker``` needs to be installed.

For local installation:
- ```pip install protobuf```

# Docker usage 

## Calculated Function
If your prefered function is not available, you have to add the function implemented in C. 
It should be named ```functionName.c``` or similar.
The C-file has to be placed in the root of the project.

## Certificates
If you want to juse certificates to improve the security, they have to be placed in the corresponiding directory. 

## On Linux, Mac OS
### Server 
Run server with ```run.sh --server``` with certificates 
or ```run.sh --server -n``` if no certifiates should be used.  

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

If you want to run the server in a docker container but the clients
locally you have to find out the ip address of the docker container.
It should be in the subnet of the ``Hyper-V Virtual Ethernet Adapter #2``
network adapter. 

# Usage

1. Put the ```cbmc-gc``` executable in the ```data/CBMC-GC-2/bin``` folder.
2. ```python3 Server.py```
3. ```python3 TwoPartyComputation.py add 4 -cn bob.mpc```
4. ```python3 TwoPartyComputation.py add 5 -cn alice.mpc```

# Instruction on variables

Every variable like (r, M[r], K[s]) and (s, M[s], K[r]) should be of
type 'bytearray'. To perform an bit wise xor operation you can use the
xor or function in the helper.py file where you can xor 2 to 4 variables.

# Information about the gate IDs
The gate IDs must always end with a zero so that the gate wires can have 
unique IDs. The input A has the id xxx0 the input B has the id xxx1 and
the output Y has the id xxx2

# Create certificates for the parties
- [Tutorial](https://legacy.thomas-leister.de/eine-eigene-openssl-ca-erstellen-und-zertifikate-ausstellen/) how to generate certificates
- Certificates should always have the ending ``-pub.pem``
- Private keys should always end on ``-key.pem``
