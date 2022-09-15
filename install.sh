#!/bin/bash
  
source clean.sh

# check if icc is present
which icc >& /dev/null
if [ $? -eq 0 ]; then
    CC=icc
else
    CC=gcc
fi

#make cpu -C svmbir/sv-mbirct/src CC=$CC

pip install -r requirements.txt
CC=$CC pip install .

#CC=$CC python setup.py bdist_wheel
#CC=$CC python setup.py build_ext --inplace

