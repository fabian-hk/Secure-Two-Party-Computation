import os

import conf


# This will only work if CBMC-GC is linked in the conf.py

def cbmc_gc_compile(ansic_file_path):
    if not os.path.isdir(conf.default_output):
        os.mkdir(conf.default_output)
    goto_location_for_output = "cd " + conf.default_output + "; "
    execute_cbmc_gc = conf.cbmc_path + " ../../../" + ansic_file_path

    # result is always stored in gate_files/default_output
    os.system(goto_location_for_output + execute_cbmc_gc + "> /dev/null 2>&1")
