#! /bin/bash
sudo apt update
sudo apt install libsilo-dev

# As of 2021-01-04, the download links at https://wci.llnl.gov/simulation/computer-codes/silo are dead.
curl -L -O https://deb.debian.org/debian/pool/main/s/silo-llnl/silo-llnl_4.10.2.real.orig.tar.xz
tar xfa silo-llnl_4.10.2.real.orig.tar.xz
sudo cp silo-llnl-4.10.2.real/src/silo/silo_exports.h /usr/include
sudo chmod a+rX /usr/include/silo_exports.h
