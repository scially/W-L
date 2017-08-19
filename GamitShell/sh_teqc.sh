#!/bin/bash
# author:wanghui
# email :wzxwhd@126.comm
# 2016-8-19

if [ $# -eq 0 ];
then
	echo "Teqc的封装，可以对某个目录下的所有Rinex文件进行批量编辑"
	echo "Usage: "
	echo "./sh_teqc.sh -file <list> -out <file> -cmd <cmd>"
	echo "    -cmd  teqc命令"
	echo "    -list 待处理的Rinex文件列表，可用 ls <dir> > list 生成"
	exit 0
fi

list=""
out=""
cmd=""

while [ $# -gt 0 ]
do
	case $1 in
		"-file") list=$2;;
		"-out")  out=$2;;
		"-cmd")  cmd=$2;;
	esac
	shift
done

echo "cmd: $cmd"
echo "out: $out"

if [ ! -e $out ];
then
	echo "$out don't exist"
	exit 0
fi

while read line
do
	teqc $cmd $line > ${out}/$line
done < $list
