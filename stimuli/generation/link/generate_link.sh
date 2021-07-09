#!/bin/bash

scenario=link
controller_dir=${3-$HOME"/tdw_physics/tdw_physics/target_controllers/"}
output_dir=${4-$HOME"/physion_data/"}

height=256
width=256

group=train
seed=0
multiplier=11.45
echo "Generating training data"
for arg_name in ./*/
do
    case $arg_name in
        (./*familiarization*) continue;;
    esac
    cmd="python3 "$controller_dir$scenario".py $arg_name""commandline_args.txt --dir "$output_dir$scenario"${arg_name#.}"$group" --height "$height" --width "$width" --seed "$seed" --save_passes '' --write_passes '_img,_id' --save_meshes --num_multiplier "$multiplier" --training_data_mode"
    echo $cmd
done

group=readout
seed=2
multiplier=5.72
echo "Generating readout data"
for arg_name in ./*/
do
    case $arg_name in
        (./*familiarization*) continue;;
    esac
    cmd="python3 "$controller_dir$scenario".py $arg_name""commandline_args.txt --dir "$output_dir$scenario"${arg_name#.}"$group" --height "$height" --width "$width" --seed "$seed" --save_passes '' --write_passes '_img,_id' --save_meshes --num_multiplier "$multiplier
    echo $cmd
done
