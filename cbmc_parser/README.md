# This parses output files of CMBC-GC ANSI-C to Logic Gate compiler
CMBC-GC Websites:
* https://forsyte.at/software/cbmc-gc/
* https://www.seceng.informatik.tu-darmstadt.de/research_seceng/software_seceng/cbmc_gc/index.en.jsp

Link PDF containing installation information and description of native circuit format:
* http://forsyte.at/wp-content/uploads/cbmc-gc-v0.9.3_upd1.pdf

CMBC-GC Repository:
* https://gitlab.com/securityengineering/CBMC-GC-2

The compiler can output different formats:
1. Bristol Format
2. Native Format
3. Fairplay Format (another such compiler which is based on Java and outputs Logic Gates as Logic Tables)

# On parse_native.py
Handles parsing of native cbmc output files by calling parse_native()

# On create_circuit.py
For parsing and circuit creation of output-files from cbmc call create_circuit_from_output_data()

example: 
create_circuit_from_output_data("add_output", Person(Person.A))
