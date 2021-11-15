#!/bin/bash

#compiler_list=("gcc" "icc" "clang")
compiler_list=("gcc" "icc")
#compiler_list=("icc")
python_version=("3.6" "3.7" "3.8" "3.9")

echo "*********************************************************"
echo "**** Building wheels" 
echo "**** Python ${python_version[@]}"
echo "**** Compilers: ${compiler_list[@]}"
echo "*********************************************************"

/bin/rm -fr dist build
/bin/rm -r svmbir.egg-info

for CC in ${compiler_list[@]}; do
    dname=dist_${CC}
    [ -d $dname ] || mkdir $dname
done

for pyv in ${python_version[@]}; do
    conda create --name sv${pyv} python=$pyv numpy Cython --yes
done

for compiler in ${compiler_list[@]}; do
    echo "****"
    echo "**** Building CMDLINE executable, CC=${compiler} " 
    echo "****"
    make -C svmbir/sv-mbirct/src CC=$compiler

    for pyv in ${python_version[@]}; do
        echo "****"
        echo "**** Building wheel for python ${pyv}, CC=${compiler} " 
        echo "****"
        conda activate sv${pyv} 
        CC=$compiler python setup.py sdist bdist_wheel
#        CC=$compiler python setup.py bdist_wheel
        conda deactivate
        mv dist/*whl dist_${compiler}
    done
done

for pyv in ${python_version[@]}; do
    conda remove --name sv${pyv} --all --yes
done

