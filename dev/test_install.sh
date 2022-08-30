#!/bin/bash

#compiler_list=("gcc" "icc" "clang")
compiler_list=("icc" "gcc")

echo "*********************************************************"
echo "**** Installing clean test environment svmbir_test ******"
echo "*********************************************************"

conda deactivate
conda remove --name svmbir_test --all
conda create --name svmbir_test python=3.8 --yes
#conda env create -f environment.yml --name svmbir_test
conda activate svmbir_test
#pip install --upgrade pip
pip install -r requirements.txt 
pip install -r demo/requirements_demo.txt

# select compiler
#CC=icc
for CC in ${compiler_list[@]}
do

echo " "
echo "***********************************************************"
echo "**** $CC : clean/build/install cython and cmdline versions " 
echo "***********************************************************"
#source clean_svmbir
/bin/rm svmbir/interface_cy_c.c
/bin/rm svmbir/*.so
/bin/rm -r build
/bin/rm -r dist
/bin/rm -r svmbir.egg-info
pip uninstall svmbir -y

make -C svmbir/sv-mbirct/src CC=$CC
CC=$CC pip install .

echo " "
echo "***********************************************************"
echo "**** $CC/cython : Running cython build_ext for pytest "
echo "***********************************************************"
CC=$CC python setup.py build_ext --inplace

echo " "
echo "***********************************************"
echo "**** $CC/cython : Running pytest "
echo "***********************************************"
pytest

echo " "
echo "****************************************************"
echo "**** $CC/cython : Running 2D Shepp-Logan demo "
echo "****************************************************"
cd demo
python demo_2D_microscopy.py
cd .. 

echo " "
echo "****************************************************"
echo "**** $CC/cmdline : Running 2D Shepp-Logan demo "
echo "****************************************************"
cd demo
CLIB=CMD_LINE python demo_2D_microscopy.py
cd .. 

done

echo ""
echo "*******************************************************"
echo "**** Deactivating/removing svmbir_test environment "
echo "*******************************************************"
conda deactivate
conda remove --name svmbir_test --all --yes


