#!/bin/bash

#-- directory of cfg files
CFG_DIR="./cfgs"
#-- directory of python files
PY_DIR="./pythons"

. $CFG_DIR/para.cfg #-- path file

scatter_CFG_DIR=$scatter_DATA_DIR

#-- scan data files in the directory
for data in $(find $scatter_DATA_DIR -mindepth 1 -maxdepth 1 -type f -name "*.dat")
do
	#--figure of memory comparison
	if [[ $data == *memory_comp.dat* ]]; then
		echo $data
		python $PY_DIR/scatter.py $data $scatter_CFG_DIR/scatter.cfg "memory comp figure"
	fi
	[ -f ${data}.eps ] && `epstopdf ${data}.eps && rm ${data}.eps`
done
