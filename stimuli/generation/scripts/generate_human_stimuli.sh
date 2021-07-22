#!/bin/bash

scenario=${1-"dominoes"}
output_dir=${2-$HOME"/physion_data"}
controller_dir=${3-"../controllers"}
gpu=${4-"0"}

echo $scenario

height=512
width=512

group=human
echo "Generating testing data"
for arg_name in ../configs/$scenario/*
do
    case $arg_name in
        (./*familiarization*) continue;;
    esac
    subdir=`echo $(basename "$arg_name")`
    cmd="python3 "$controller_dir"/"$scenario".py @$arg_name""/commandline_args.txt --dir "$output_dir"/"$scenario"/"$group"/"$subdir" --height "$height" --width "$width" --save_passes '_img' --write_passes '_img,_id' --gpu "$gpu
    echo $cmd
    eval " $cmd"
done
