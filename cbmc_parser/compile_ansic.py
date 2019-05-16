import os

from conf import conf


# This will only work if CBMC-GC is linked in the conf.py

def cbmc_gc_compile(ansic_file_path):
    """
    Function that will call CBMC-GC for compiling a .c file and create output.* files representing the circuit

    :param ansic_file_path: name of the ANSI-C .c file that is compiled
    :return: nothing is returned - results are saved to cbmc_parser/gate_files/default_output
    """
    if not os.path.isdir(conf.default_output):
        os.mkdir(conf.default_output)

    execute_cbmc_gc = conf.cbmc_path + "cbmc-gc " + ansic_file_path

    # result is always stored in gate_files/default_output
    os.system(execute_cbmc_gc + " --outdir " + conf.default_output)
