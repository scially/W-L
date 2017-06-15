#!/bin/bash
#author:wanghui
#email:wzxwhd@126.com
#introduce
if [ $# -eq 0 ];then
    echo "================================================================="
    echo "this shell will call sh_rx2apr to apply "
    echo "files from current path, and is only to "
    echo "use svpos."
    echo "use ./sh_lfile.sh -nav <nav> -ref <ref> -apr <apr> -yr <year> -doy <doy>"
    echo "         -chi <val>"
    echo "required paramers:"
    echo "	   -yr"
    echo "	   -doy"
    echo "Note that the <site> file must be within or linked in  the"
    echo "current directory (no pathname allowed)."
    echo "================================================================="
    exit 1
fi
rm -f lfile.apr
args=$@
year=""
doy=""
apr=""
while [ $# -gt 0 ]
do
    case $1 in
    "-apr")
    apr=$2;;
    "-yr")
    year=$2;;
    "-doy")
    doy=$2;;
    esac
    shift
done
regmatch="[a-zA-Z0-9]{4}${doy}0.${year:0-2:2}o"
for file in `ls`
do
   if [[ $file =~ $regmatch ]];then
	site=${file:0:4}
	cmd_temp="sh_rx2apr -site ${file} "$args
	echo $cmd_temp
        ${cmd_temp} 1>/dev/null
	cat ${site}.apr >> lfile.apr
	rm -f ${site}.apr lfile.${site}
   fi
done
echo "Output file:lfile.apr"