import os

#This will only work if CBMC-GC is installed

#path from destination of this file to CBMC-GC root directory
path_to_cbmc = "../../../../CBMC-GC-2-master"
#filename of ansi c file in ansi_c_code directory that is compiled to gates 
ansic_filename = "addition.c"

def cbmc_gc_compile(path_to_cbmc, ansic_filename):
	goto_location_for_output = "cd gate_files/default_output; " 
	execute_cbmc_gc = "./" + path_to_cbmc + "/bin/cbmc-gc ../../ansi_c_code/" + ansic_filename +"; "

	#result is always stored in gate_files/default_output
	os.system(goto_location_for_output + execute_cbmc_gc)

cbmc_gc_compile(path_to_cbmc, ansic_filename)
