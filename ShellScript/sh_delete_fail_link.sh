#!/bin/bash

if [ $# -eq 0 ];then
    echo "detect and delete corrupted link"
    echo "Usage:"
    echo " ./.sh -path <path>"
    exit 1
fi

function pathjoin(){
    local path
    path=""
    while [ $# -gt 1 ]
    do
        if [ ${1:0-1} == "/" ];then
            path="${path}$1"
        else
            path="${path}$1""/"
        fi 
        shift
    done
    echo "${path}""$1"
}

path=""
while [ $# -gt 0 ]
do
    case $1 in 
	"-path") path=$2;;
    esac    
    shift
done

list=`ls $path`
for var in ${list[@]}
do
    filename=`pathjoin $path $var`
    if [ ! -e $filename ]; then
        echo "$filename不存在,即将删除"
        rm -f $filename
    fi
done
