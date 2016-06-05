#!/bin/bash

#-- directory of cfg files
CFG_DIR="../cfgs"
#-- directory of python files
PY_DIR="../pythons"

. $CFG_DIR/para.test.cfg #-- path file

bar_CFG_DIR=$bar_DATA_DIR

#-- scan data files in the directory
for data in $(find $bar_DATA_DIR -mindepth 1 -maxdepth 1 -type f -name "*.dat")
do
	#--figure of read ratio
	if [[ $data == *read_ratio.dat* ]]; then
		echo $data
		python $PY_DIR/bar.py $data $bar_CFG_DIR/bar.cfg "read ratio figure"
	fi

	#--figure of cycles
	if [[ $data == *paper.stat_cycles* ]]; then
		echo $data
        python $PY_DIR/bar.py $data $bar_CFG_DIR/bar.cfg "time figure"
	fi

	#--figure of lat
	if [[ $data == *stat_comp_lat* ]]; then
		echo $data
		python $PY_DIR/bar.py $data $bar_CFG_DIR/bar.cfg "read latency figure"
	fi

	#--figure of EDP
	if [[ $data == *stat_energyEDP* ]]; then
		echo $data
		python $PY_DIR/bar.py $data $bar_CFG_DIR/bar.cfg "EDP figure"
	fi

	#--convert to pdf and remove the eps file
	[ -f ${data}.eps ] && `$EPS2PDF ${data}.eps && rm ${data}.eps`
done
