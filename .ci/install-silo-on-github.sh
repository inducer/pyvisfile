#! /bin/bash
sudo apt update
sudo apt install libsilo-dev

curl -L -O https://wci.llnl.gov/content/assets/docs/simulation/computer-codes/silo/silo-4.10.2/silo-4.10.2-bsd-smalltest.tar.gz
tar xfz silo-4.10.2-bsd-smalltest.tar.gz
sudo cp silo-4.10.2-bsd/src/silo/silo_exports.h /usr/include
sudo chmod a+rX /usr/include/silo_exports.h
