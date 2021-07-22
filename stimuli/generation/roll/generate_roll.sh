#!/bin/bash

scenario=roll
output_dir=${1-$HOME"/physion_data"}
controller_dir=${2-$HOME"/tdw_physics"}

height=256
width=256

group=train
seed=0
multiplier=11
echo "Generating training data"
for arg_name in ./*/
do
    case $arg_name in
        (./*familiarization*) continue;;
    esac
    if [[ $arg_name == *"collision"* ]]
    then
        controller="$controller_dir""/tdw_physics/target_controllers/"collide
    else
        controller=$controller_dir"/tdw_physics/target_controllers/"$scenario
    fi
    cmd="python3 "$controller".py @$arg_name""commandline_args.txt --dir "$output_dir"/"$scenario"${arg_name#.}"$group" --height "$height" --width "$width" --seed "$seed" --save_passes '' --write_passes '_img,_id' --save_meshes --num_multiplier "$multiplier" --training_data_mode"
    echo $cmd
    eval " $cmd"
done

group=readout
seed=2
multiplier=5.5
echo "Generating readout data"
for arg_name in ./*/
do
    case $arg_name in
        (./*familiarization*) continue;;
    esac
    if [[ $arg_name == *"collision"* ]]
    then
        controller="$controller_dir""/tdw_physics/target_controllers/"collide
    else
        controller=$controller_dir"/tdw_physics/target_controllers/"$scenario
    fi
    cmd="python3 "$controller".py @$arg_name""commandline_args.txt --dir "$output_dir"/"$scenario"${arg_name#.}"$group" --height "$height" --width "$width" --seed "$seed" --save_passes '' --write_passes '_img,_id' --save_meshes --num_multiplier "$multiplier" --readout_data_mode"
    echo $cmd
    eval " $cmd"
done
