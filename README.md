# Installation
Dependencies:
- ```pip install protobuf```

# Usage example
1. You have to set the ``crt_storage`` variable to your 
certification folder in the ``conf.py`` file
2. ```python3 Server.py```
3. ```python3 TwoPartyComputation.py and_op 42 certification-alice bob.mpc```
4. ```python3 TwoPartyComputation.py and_op 42 certification-bob alice.mpc```

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
- Certificates should allways have the ending ``-pub.pem``
- Private keys should allways end on ``-key.pem``