# Installation
Dependencies:
- ```pip install protobuf```

# Usage example
1. ```python3 Server.py```
2. ```python3 TwoPartyComputation.py and_op 42```
3. ```python3 TwoPartyComputation.py and_op 42```

# Instruction on variables

Every variable like (r, M[r], K[s]) and (s, M[s], K[r]) should be of
type 'bytearray'. To perform an bit wise xor operation you can use the
xor or function in the helper.py file where you can xor 2 to 4 variables.

# Information about the gate IDs
The gate IDs must always end with a zero so that the gate wires can have 
unique IDs. The input A has the id xxx0 the input B has the id xxx1 and
the output Y has the id xxx2