# Adaptive Noise Canceler for GnuRadio

Adaptive Noise Canceler is a GnuRadio module implemented in Python for the final project of the course "Comunicaciones Inalámbricas" (IIE, FING, UdelaR - 2017/2018).

Installation procedure:

1. Download git files, rename anc folder to gr-comina.

2. Enter gr-comina and write these commands:

mkdir build

cd build

cmake ../

make

make test

sudo make install

sudo ldconfig

There are some example files in examples folder, the PATH towards the wav files must be updated in order to work.