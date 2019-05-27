# Parser

- Parsing the output from CBMC-GC and building the datastructure of the circuit required for the protocol is handled in this folder.
- Example C-Code and the corresponding output from CBMC-GC can be found in this folder.

# Information on CBMC-GC (C Bounded Model Checker - Garbled Circuits)

CBMC-GC Websites:
* https://forsyte.at/software/cbmc-gc/
* https://www.seceng.informatik.tu-darmstadt.de/research_seceng/software_seceng/cbmc_gc/index.en.jsp

PDF containing installation information for CBMC-GC and description of native circuit format can be found [here](http://forsyte.at/wp-content/uploads/cbmc-gc-v0.9.3_upd1.pdf).

CBMC-GC Repository:
* https://gitlab.com/securityengineering/CBMC-GC-2


The compiler can output different formats:
1. Bristol Format
2. Native Format
3. Fairplay Format (another such compiler which is based on Java and outputs Logic Gates as Logic Tables)

We use the Native Format of CBMC-GC for our project.

