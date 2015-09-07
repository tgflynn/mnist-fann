# mnist-fann
A C program which uses libfann to train a simple MLP on MNIST

MNIST Data: http://yann.lecun.com/exdb/mnist/

Platform: Ubuntu 14.04

Dependencies:

  sudo apt-get install gcc
  sudo apt-get install libfann2 libfann-dbg
  

Files:

  typescript - Example training output with classificaation error on test set

  train2.c - The trainer

    Compilation: 
      gcc -o train2 train2.c -lfann

    Usage:
      Expects files train.fann and test.fann in working directory

      ./train2

   idxToCsv.py: Converts MNIST binary data files to libfann compatible text format.

    Usage: ./idxToCsv.py -h - Show help

      Example:

        ./idxToCsv.py -i train-images-idx3-ubyte -l train-labels-idx1-ubyte -o train.fann
        ./idxToCsv.py -i t10k-images-idx3-ubyte -l t10k-labels-idx1-ubyte -o test.fann
