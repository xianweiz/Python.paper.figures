#!/bin/bash

#-- directory of cfg files
CFG_DIR="../cfgs"
#-- directory of python files
PY_DIR="../pythons"

. $CFG_DIR/para.test.cfg #-- path file

log_line_CFG_DIR=$log_line_DATA_DIR

#-- scan data files in the directory
for data in $(find $log_line_DATA_DIR -mindepth 1 -maxdepth 1 -type f -name "*.dat")
do
	#--figure of ret failure probability
	if [[ $data == *ret.dat* ]]; then
		echo $data
		python $PY_DIR/log_line.py $data $log_line_CFG_DIR/log_line.cfg "ret prob figure"
	fi
	
	[ -f ${data}.eps ] && `$EPS2PDF ${data}.eps && rm ${data}.eps`
done
