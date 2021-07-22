#!/bin/bash

scenario=${1-"dominoes"}
output_dir=${2-$HOME"/physion_data"}
controller_dir=${3-"../controllers"}
gpu=${4-"0"}

echo $scenario

height=256
width=256

group=test
echo "Generating testing data"
for arg_name in ../configs/$scenario/*/
do
    case $arg_name in
        (./*familiarization*) continue;;
    esac
    cmd="python3 "$controller_dir"/"$scenario".py @$arg_name""commandline_args.txt --dir "$output_dir"/"$scenario"${arg_name#.}"$group" --height "$height" --width "$width" --save_passes '' --write_passes '_img,_id,_depth,_normals,_flow' --save_meshes --testing_data_mode --gpu "$gpu
    echo $cmd
    eval " $cmd"
done
