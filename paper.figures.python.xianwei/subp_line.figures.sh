#!/bin/bash

#-- directory of cfg files
CFG_DIR="./cfgs"
#-- directory of python files
PY_DIR="./pythons"

. $CFG_DIR/para.cfg #-- path file

subp_line_CFG_DIR=$subp_line_DATA_DIR

#-- scan data files in the directory
for data in $(find $subp_line_DATA_DIR -mindepth 1 -maxdepth 1 -type f -name "*.dat")
do
	#--figure of switch
	if [[ $data == *switch.dat* ]]; then
		echo $data
		python $PY_DIR/subp_line.py $data $subp_line_CFG_DIR/subp_line.cfg "switch figure"
	fi

	[ -f ${data}.eps ] && `epstopdf ${data}.eps && rm ${data}.eps`
done

