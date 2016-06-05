#!/bin/bash

#-- directory of cfg files
CFG_DIR="./cfgs"
#-- directory of python files
PY_DIR="./pythons"

. $CFG_DIR/para.cfg #-- path file

my_DATA_DIR=$memsys_DATA_DIR
#-- scan data files in the directory
my_CFG_DIR=$my_DATA_DIR

#-- moti figure
for data in `find $my_DATA_DIR -mindepth 1 -maxdepth 1 -type f -name "*.dat"`
do
    if [[ $data == *rst.dat ]]; then
        echo $data
        python $PY_DIR/y2.py $data $my_CFG_DIR/y2.cfg "perf_energy figure"
    fi

    if [[ $data == *qos.dat ]]; then
        echo $data
        python $PY_DIR/bar.py $data $my_CFG_DIR/bar.cfg "qos figure"
    fi

    [ -f ${data}.eps ] && `$EPS2PDF ${data}.eps && rm ${data}.eps`
done
