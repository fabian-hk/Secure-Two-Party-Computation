# Instruction to run the program
1. run fpre_server.py
2. run user_a.py
3. run user_b.py

# Instruction on variables

Every variable like (r, M[r], K[s]) and (s, M[s], K[r]) should be of
type 'bytearray'. To perform an bit wise xor operation you can use the
xor or function in the helper.py file where you can xor 2 to 4 variables.

# Information about the gate IDs
The gate IDs must always end with a zero. So that the gate wires can have 
unique IDs. The input A has the id xxx0 the input B has the id xxx1 and
the output Y has the id xxx2