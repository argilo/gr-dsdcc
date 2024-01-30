gr-dsdcc
========

Author: Clayton Smith  
Email: <argilo@gmail.com>

The goal of this project is to package DSDcc (Digital Speech Decoder) as
a GNU Radio block, so that it can be easily used with software radio
peripherals such as the Ettus Research USRP or RTL2832U-based USB TV
tuners.

Dependencies:

  * GNU Radio 3.10
  * DSDcc (https://github.com/f4exb/dsdcc)
  * mbelib (https://github.com/szechyjs/mbelib)

Build instructions:

    mkdir build
    cd build
    cmake ..
    make
    sudo make install
    sudo ldconfig

After running the above commands, "DSDcc Block" should appear under the
"DSDcc" category in GNU Radio Companion, and "dsdcc_block" will be available
in the "dsdcc" Python package.

The block expects 48000 samples per second input, and outputs sound at
8000 samples per second.  The input should be FM-demodulated (for
example, with GNU Radio's Quadrature Demod block) and should be between
-1 and 1 while receiving digital signals.  The input signal should
also be free of DC bias, so make sure you are tuned accurately, or
filter out DC.

Contributions are welcome!
