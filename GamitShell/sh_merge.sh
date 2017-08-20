#!/bin/bash
# author:wanghui
# email:wzxwhd@126.com

# updated by wanghui 2017/8/19
# updated by wanghui 2017/8/20
if [ $# -eq 0 ];then
    echo "Merge rinex files by teqc and make track.cmd"
    echo "Usage ./sh_merge.sh -year <year> -doy <doy> -regx <regx> -file <list> -out <file>"
    echo "-file <list> is a list of the merging site"
    exit 1
fi

regx=""
year=""
doy=""
list=""
out="./track"

while [ $# -gt 0 ]
do
    case $1 in 
	"-year") year=$2;;
	"-doy")  doy=$2;;
	"-file") list=$2;;
	"-regx") regx=$2;;
	"-out")  out=$2;;
    esac    
    shift
done

if [ -z $doy ] || [ -z $year ];   #  equal to "$doy"=="" || "$year"==""
then
	echo "doy and year is required!"
	exit 1
fi
if [ ! -e track ];
then 
    mkdir $out
fi

echo "@OBS_FILE" >> track/track.cmd
echo " obs_file" >> track/track.cmd
while read line
do
    if [ ${#line} -ge 6 ] && [ ${line:5:1} == "F" ];
    then
	    echo "  ${line:0:4} ${line:0:4}${doy}0.${year:2:2}o F" >> ${out}/track.cmd
    elif [ ${#line} -eq 4 ] || [ ${line:5:1} == "K" ];
    then
	    echo "  ${line:0:4} ${line:0:4}${doy}0.${year:2:2}o K" >> ${out}/track.cmd
    fi
    teqc ${line:0:4}$doy$regx.${year:2:2}[Oo] > "${out}/${line:0:4}${doy}0.${year:2:2}o"
done < $list
