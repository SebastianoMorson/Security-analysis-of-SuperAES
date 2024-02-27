# Super AES

The Super AES implementation is based on Frank Hemworth's higher order masked implementation (github/knarfrank). 

This implementation is free to use and implements the strongest countermeasure against DPA style attacks. The implementation can compile with gcc but it is already targeted for the Cortex M0 processor and therefore can be crosscompiled to the M0.

We embedd some functions to test the implementation in the leakage emulator GILES (github/sca-research/GILES). 


# Getting Started

We provide a makefile compatible with CMAKE.
Copy this folder into the same folder as GILES is in. 

Assuming that GILES and therefore also thumb-sim are installed:

Compile your programm with 

make -C SuperAES

Run your program with 

pathto/thumb-sim -b SuperAES/SuperAES.bin

Use GILES to produce power traces or do fault analysis via

pathto/GILES pathto/SuperAES.bin -o test.trs


# License - MIT (Expat)

This project is licensed under the MIT (Expat) License - see the [LICENSE](LICENSE) file for details.

All contributions are welcome.
Please let me know if you find any bugs, especially inaccuracies in the timing of an operation.
