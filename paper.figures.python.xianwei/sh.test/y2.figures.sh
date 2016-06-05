#!/bin/bash

#-- directory of cfg files
CFG_DIR="../cfgs"
#-- directory of python files
PY_DIR="../pythons"

. $CFG_DIR/para.test.cfg #-- path file

y2_CFG_DIR=$y2_DATA_DIR

#-- scan data files in the directory
for data in $(find $y2_DATA_DIR -mindepth 1 -maxdepth 1 -type f -name "*.dat")
do
	#--figure of fixlane
	if [[ $data == *moti_fixlane.dat* ]]; then
		echo $data
		python $PY_DIR/y2.py $data $y2_CFG_DIR/y2.cfg "fixlane figure"
	fi

	#--figure of fixratio
	if [[ $data == *moti_fixratio.dat* ]]; then
		echo $data
        python $PY_DIR/y2.py $data $y2_CFG_DIR/y2.cfg "fixratio figure"
	fi

	[ -f ${data}.eps ] && `$EPS2PDF ${data}.eps && rm ${data}.eps`
done
