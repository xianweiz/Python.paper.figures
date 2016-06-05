#!/bin/bash

#-- directory of cfg files
CFG_DIR="./cfgs"
#-- directory of python files
PY_DIR="./pythons"

. $CFG_DIR/para.cfg #-- path file

my_DATA_DIR=$todaes_DATA_DIR
#-- scan data files in the directory
my_CFG_DIR=$my_DATA_DIR

#-- moti figure
for data in $(find $my_DATA_DIR -mindepth 1 -maxdepth 1 -type f -name "*moti.dat")
do
	if [[ $data == *moti.dat ]]; then
		echo $data
		python $PY_DIR/y2.py $data $my_CFG_DIR/y2.cfg "moti figure"
	fi

	[ -f ${data}.eps ] && `$EPS2PDF ${data}.eps && rm ${data}.eps`
done

#-- main general figures
for data in $(find $my_DATA_DIR -mindepth 1 -maxdepth 1 -type f -name "*.dat")
do
    #--figure of access profiling
    if [[ $data == *page* ]]; then
        echo $data
        python $PY_DIR/usual_line.py $data $my_CFG_DIR/usual_line.cfg "access line figure"
        bar_dat_file=$data".bar"
        `cp $data $bar_dat_file`
        python $PY_DIR/bar.py $bar_dat_file $my_CFG_DIR/bar.cfg "access bar figure"
        [ -f ${bar_dat_file}.eps ] && `$EPS2PDF ${bar_dat_file}.eps && rm ${bar_dat_file}.eps`
    fi

    if [[ $data == *journal_avgLat* ]]; then
        echo $data
        python $PY_DIR/bar.py $data $my_CFG_DIR/bar.cfg "access latency figure"
    fi

    if [[ $data == *journal_spare* ]]; then
        echo $data
        python $PY_DIR/bar.py $data $my_CFG_DIR/bar.cfg "sense spare figure"
    fi

    if [[ $data == *journal_chunk* ]]; then
        echo $data
        python $PY_DIR/bar.py $data $my_CFG_DIR/bar.cfg "sense chunk figure"
    fi

	[ -f ${data}.eps ] && `$EPS2PDF ${data}.eps && rm ${data}.eps`
done

#-- 14nm figures
for data in $(find $my_DATA_DIR/14nm -mindepth 1 -maxdepth 1 -type f -name "*.dat")
do
    #--main figure of 14nm PROF journal
    if [[ $data == *stat_PROF_main-cycles.perc* ]]; then
        echo $data
		path=`dirname $data`
		prof_small_file=$path/"PROF_small.dat"
        [ -f $prof_small_file ] || `cp $data $prof_small_file`
        python $PY_DIR/bar.py $data $my_CFG_DIR/bar.cfg "14nm PROF figure"
    fi

    #--main figure of 14nm RAND journal
    if [[ $data == *stat_RAND_main-cycles.perc* ]]; then
        echo $data
		path=`dirname $data`
		rand_small_file=$path/"RAND_small.dat"
        [ -f $rand_small_file ] || `cp $data $rand_small_file`
        python $PY_DIR/bar.py $data $my_CFG_DIR/bar.cfg "14nm RAND figure"
    fi

    #--main figure of 14nm RAND-PROF journal
    if [[ $data == *RAND_small* ]]; then
        echo $data
        python $PY_DIR/bar.py $data $my_CFG_DIR/bar.cfg "14nm RAND-PROF figure"
    fi

    #--main figure of 14nm RAND-PROF journal
    if [[ $data == *PROF_small* ]]; then
        echo $data
        python $PY_DIR/bar.py $data $my_CFG_DIR/bar.cfg "14nm RAND-PROF figure"
    fi

    [ -f ${data}.eps ] && `$EPS2PDF ${data}.eps && rm ${data}.eps`
done

#-- 20nm figures
for data in $(find $my_DATA_DIR/20nm -mindepth 1 -maxdepth 1 -type f -name "*.dat")
do
    #--main figure of 20nm PROF journal
    if [[ $data == *stat_PROF_main-cycles.perc* ]]; then
        echo $data
		path=`dirname $data`
		prof_small_file=$path/"PROF_small.dat"
        [ -f $prof_small_file ] || `cp $data $prof_small_file`
        python $PY_DIR/bar.py $data $my_CFG_DIR/bar.cfg "20nm PROF figure"
    fi

    #--main figure of 20nm RAND journal
    if [[ $data == *stat_RAND_main-cycles.perc* ]]; then
        echo $data
		path=`dirname $data`
		rand_small_file=$path/"RAND_small.dat"
        [ -f $rand_small_file ] || `cp $data $rand_small_file`
        python $PY_DIR/bar.py $data $my_CFG_DIR/bar.cfg "20nm RAND figure"
    fi

    #--main figure of 20nm RAND-PROF journal
    if [[ $data == *RAND_small* ]]; then
        echo $data
        python $PY_DIR/bar.py $data $my_CFG_DIR/bar.cfg "20nm RAND-PROF figure"
    fi

    #--main figure of 20nm RAND-PROF journal
    if [[ $data == *PROF_small* ]]; then
        echo $data
        python $PY_DIR/bar.py $data $my_CFG_DIR/bar.cfg "20nm RAND-PROF figure"
    fi


	[ -f ${data}.eps ] && `$EPS2PDF ${data}.eps && rm ${data}.eps`
done
