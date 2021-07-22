#!/bin/bash

scenario=${1-"dominoes"}
output_dir=${2-$HOME"/physion_data"}
controller_dir=${3-"../controllers"}
gpu=${4-"0"}

case $scenario in
    "dominoes")
	tmult=7.25
	rmult=3.62
	;;
    "support")
	tmult=9.1
	rmult=4.55
	;;
    "collide")
	tmult=5.9
	rmult=2.94
	;;
    "contain")
	tmult=11.45
	rmult=5.72
	;;
    "drop")
	tmult=10
	rmult=5
	;;
    "roll")
	tmult=11
	rmult=5.5
	;;
    "link")
	tmult=11.45
	rmult=5.72
	;;
    "drape")
	tmult=11.11
        rmult=5.55
	;;
    *)
	echo "Usage:\n./generate_train_and_readout_data.sh SCENARIO [OUTPUT_DIR] [CONTROLLER_DIR]"
	echo "Valid SCENARIOs: {dominoes, support, collide, contain, drop, roll, link, drape}"
	exit 1
	;;
esac

echo $scenario
echo $tmult
echo $rmult

height=256
width=256

group=train
seed=0
echo "Generating training data"
for arg_name in ../configs/$scenario/*/
do
    case $arg_name in
        (./*familiarization*) continue;;
    esac
    cmd="python3 "$controller_dir"/"$scenario".py @$arg_name""commandline_args.txt --dir "$output_dir"/"$scenario"${arg_name#.}"$group" --height "$height" --width "$width" --seed "$seed" --save_passes '' --write_passes '_img,_id' --save_meshes --num_multiplier "$tmult" --training_data_mode --gpu "$gpu
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
    cmd="python3 "$controller_dir"/"$scenario".py @$arg_name""commandline_args.txt --dir "$output_dir"/"$scenario"${arg_name#.}"$group" --height "$height" --width "$width" --seed "$seed" --save_passes '' --write_passes '_img,_id' --save_meshes --num_multiplier "$rmult" --readout_data_mode --gpu "$gpu
    echo $cmd
    eval " $cmd"
done
