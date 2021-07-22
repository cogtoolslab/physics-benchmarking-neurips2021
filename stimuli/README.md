## Generating training and readout data

1. Install [`tdw_physics`](https://github.com/neuroailab/tdw_physics/tree/master) following the instructions
2. Bash scripts for generating both training and readout data can be found in their corresponding subdirectories under `generation` (i.e. `./generation/[SCENARIO]/generate_[SCENARIO].sh`)
   1. The script takes two *positional* args, the first being the absolute path to where you want the output data saved. Default is `$HOME/physion_data`.
   2. The second is the absolute path to the `tdw_physics` repo on the system. Default is `$HOME/tdw_physics`.
## Notes
Each scenario's directory (`./generation/[SCENARIO]`) contains subdirectories that correspond to different sets of "args" passed to the controller. Collectively, these args determine the types of scenes in each scenario. The actual command line args are located in the `./generation/[SCENARIO]/[ARG_NAME]/commandline_args.txt` file. 

N.B. Some args correspond to the familiarization trials and are not used for generating the training and readout data. 

A `mutliplier` is set for each specific arg setting to ensure that approximately 2000 trials are generated for training and 1000 trials for the readout. 

Controllers for each scenario are located in the previously mentioned [`tdw_physics`](https://github.com/neuroailab/tdw_physics/tree/master) repo, in [`tdw_physics/target_controllers`](https://github.com/neuroailab/tdw_physics/tree/master/tdw_physics/target_controllers).
