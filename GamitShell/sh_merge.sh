#!/bin/bash
#author:wanghui
#email:wzxwhd@126.com

if [ $# -eq 0 ];then
    echo "Merge rinex files by teqc and make track.cmd"
    echo "Usage ./sh_merge.sh -year <year> -doy <doy> -time <stamp> -file <list> "
    echo "-file <list> is a list of the merging site"
    exit 0
fi

stamp=(A)
year=2016
doy=318
list=""

while [ $# -gt 0 ]
do
    case $1 in 
	"-year") year=$2;;
	"-doy")  doy=$2;;
	"-file") list=$2;;
	"-time")
	       	stamp=(`echo $@ | cut -d '-' -f2`)
		stamp=${stamp#${stamp[0]}}
    esac    
    shift
done

reg=""
for str in ${stamp[@]}
do
    reg=$reg$str
done
#将创建track目录
#请确保你的track目录无任何重要文件
if [ -e track ];
then 
    rm -rf track
fi
mkdir track
echo "@OBS_FILE" >> track/track.cmd
echo " obs_file" >> track/track.cmd
while read line
do
    if [ ${#line} -ge 6 ] && [ ${line:5:1} == "F" ];
    then
	    echo "  ${line:0:4} ${line:0:4}$doy0.${year:2:2}o F" >> track/track.cmd
    elif [ ${#line} -eq 4 ] || [ ${line:5:1} == "K" ];
    then
	    echo "  ${line:0:4} ${line:0:4}$doy0.${year:2:2}o K" >> track/track.cmd
    fi
    teqc -R -E -S ${line:0:4}$doy[$reg]*.${year:2:2}[Oo] > "track/${line:0:4}${doy}0.${year:2:2}o"
done < $list
