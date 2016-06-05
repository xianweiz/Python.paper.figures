#!/bin/bash

#-- directory of cfg files
CFG_DIR="../cfgs"
#-- directory of python files
PY_DIR="../pythons"

. $CFG_DIR/para.test.cfg #-- path file

line_CFG_DIR=$line_DATA_DIR

#-- scan data files in the directory
for data in $(find $line_DATA_DIR -mindepth 1 -maxdepth 1 -type f -name "*.dat")
do
	#--figure of stress
	if [[ $data == *stress_3B.dat* ]]; then
		echo $data
		python $PY_DIR/line.py $data $line_CFG_DIR/line.cfg "stress figure"
	fi

	#--figure of bandwidth
	if [[ $data == *bw.dat* ]]; then
		echo $data
		python $PY_DIR/line.py $data $line_CFG_DIR/line.cfg "bw figure"
	fi

	#--figure of usual line
	if [[ $data == *page.dat* ]]; then
		echo $data
		python $PY_DIR/usual_line.py $data $line_CFG_DIR/usual_line.cfg "access line figure"
	fi

	[ -f ${data}.eps ] && `$EPS2PDF ${data}.eps && rm ${data}.eps`
done
