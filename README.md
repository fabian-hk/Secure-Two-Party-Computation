# Installation
Dependencies:
- ```Docker``` needs to be installed.

# Usage 
## Calculated Function
If your prefered function is not available, you have to add the function implemented in C. 
It should be named ```functionName.c``` or similar.
The C-file has to be placed in the root of the project.

## Certificates
If you want to juse certificates to improve the security, they have to be placed in the corresponiding directory. 

## On Linux, Mac OS
After the steps above, generate docker container with the corresponding ```setup_server.sh```, ```setup_client_base.sh```, ```setup_alice.sh``` and ```setup_bob.sh```. 
The client_base needs to be generated on every machine which runs alice or bob.  
If all the containers need to be generated on a single machine just execute ```renew_docker.sh```. 

To run the Server use ```run_server.sh```, if there is no need for certificates run ```run_server.sh -n```.  

To run the client use ```run_alice``` or ```run_bob.sh```





## Windows



1. In the ``conf.py`` file you have to set the ``crt_storage`` variable to your 
certification folder  and the ``cbmc_path``
variable to the ``bin`` folder in which the ``cbmc-gc`` executable is 
.
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
