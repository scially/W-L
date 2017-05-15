#/bin/bash
#author:wanghui
#email:wzxwhd@126.com
#introduce
if [ $# -eq 0 ];then
 echo "update the rinex files to station.info"
 echo "firstly,you need to ready a station.info model"
 echo "Looking forward that you give me a new method for this shell"
 echo "use ./sh_update_stnfo.sh -yr <year>"
 exit
fi
echo "sh_update_stnfo version 2017/4/27"
echo "Input Option:$@"
year=""
while [ $# -gt 0 ]
do
 case $1 in
  "-yr")
  year=$2
  ;;
 esac
 shift
done
for file in `ls`
do
	if [[ $file =~ [a-zA-Z0-9]{8}.${year:0-2:2}o ]];then
	echo "update $file"
	sh_upd_stnfo -files $file >> updation.log
	fi
done
