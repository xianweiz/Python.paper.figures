#!/bin/bash

#-- directory of cfg files
CFG_DIR="../cfgs"
#-- directory of python files
PY_DIR="../pythons/func"

. $CFG_DIR/para.test.cfg #-- path file

func_CFG_DIR=$func_DATA_DIR

#-- func_data has no use, just for argument consistency
[ -d $func_DATA_DIR ] || mkdir $func_DATA_DIR

func_names="rc leak tret_20nm tret_60nm"

for func_name in $func_names
do
	echo "=======> $func_name"

	func_data=$func_DATA_DIR/"${func_name}.dat"

	if [[ $func_name == tret_* ]]; then
		python $PY_DIR/${func_name}.py $func_data $func_CFG_DIR/tret.cfg "ret figure"
	else
		python $PY_DIR/${func_name}.py $func_data $func_CFG_DIR/${func_name}.cfg "${func_name} figure"
	fi

	[ -f ${func_data}.eps ] && `$EPS2PDF ${func_data}.eps && rm ${func_data}.eps`
done
