#!/bin/bash

scenario=${1-"dominoes"}
output_dir=${2-$HOME"/physion_data"}
controller_dir=${3-"../controllers"}

height=256
width=256

group=train
seed=0
multiplier=5.9 # 2000/340
echo "Generating training data"
for arg_name in ../configs/$scenario/*/
do
    case $arg_name in
        (./*familiarization*) continue;;
    esac
    cmd="python3 "$controller_dir"/"$scenario".py @$arg_name""commandline_args.txt --dir "$output_dir"/"$scenario"${arg_name#.}"$group" --height "$height" --width "$width" --seed "$seed" --save_passes '' --write_passes '_img,_id' --save_meshes --num_multiplier "$multiplier" --training_data_mode"
    echo $cmd
    eval " $cmd"
done

group=readout
seed=2
multiplier=2.94 # 1000/340
echo "Generating readout data"
for arg_name in ../configs/$scenario/*/
do
    case $arg_name in
        (./*familiarization*) continue;;
    esac
    cmd="python3 "$controller_dir"/"$scenario".py @$arg_name""commandline_args.txt --dir "$output_dir"/"$scenario"${arg_name#.}"$group" --height "$height" --width "$width" --seed "$seed" --save_passes '' --write_passes '_img,_id' --save_meshes --num_multiplier "$multiplier" --readout_data_mode"
    echo $cmd
    eval " $cmd"
done
