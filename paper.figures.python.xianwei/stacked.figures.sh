#!/bin/bash

#-- directory of cfg files
CFG_DIR="./cfgs"
#-- directory of python files
PY_DIR="./pythons/stacked"

. $CFG_DIR/para.cfg #-- path file

stacked_CFG_DIR=$stacked_DATA_DIR

#-- scan data files in the directory
for data in $(find $stacked_DATA_DIR -mindepth 1 -maxdepth 1 -type f -name "*.dat")
do
	#--figure of '2scheme3case'
	if [[ $data == *stack_2scheme3case.dat* ]]; then
		echo $data
		python $PY_DIR/stacked_1.py $data $stacked_CFG_DIR/stacked.cfg "write 2scheme3case figure"
	fi

	#--figure of '3scheme2case'
	if [[ $data == *stack_3scheme2case.dat* ]]; then
		echo $data
		python $PY_DIR/stacked_1.py $data $stacked_CFG_DIR/stacked.cfg "write 3scheme2case figure"
	fi

	#--figure of '4scheme3case', type1
	if [[ $data == *stack_4scheme3case.dat* ]]; then
		echo $data
		python $PY_DIR/stacked_1.py $data $stacked_CFG_DIR/stacked.cfg "write 4scheme3case figure"
	fi

	#--figure of '4scheme3case', type2
	if [[ $data == *stack_4scheme3case.type2.dat* ]]; then
		echo $data
		python $PY_DIR/stacked_2.py $data $stacked_CFG_DIR/stacked.cfg "write 4scheme3case figure - type2"
	fi

	[ -f ${data}.eps ] && `epstopdf ${data}.eps && rm ${data}.eps`
done
