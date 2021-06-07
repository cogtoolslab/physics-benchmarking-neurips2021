# human-physics-benchmarking

## Dataset generation

This repo depends on outputs from [`tdw_physics`](https://github.com/threedworld-mit/tdw).

Specifically, [`tdw_physics`](https://github.com/threedworld-mit/tdw) is used to generate the dataset of physical scenarios (a.k.a. stimuli), including both the **training datasets** used to train physical-prediction models, as well as **test datasets** used to measure prediction accuracy in both physical-prediction models and human participants.

## Modeling experiments
This repo depends on outputs from [`physopt`](https://github.com/neuroailab/physopt-physics-benchmarking).

The [`physopt`](https://github.com/neuroailab/physopt-physics-benchmarking) repo was used to conduct physical-prediction model training and evaluation. 

## Human experiments

This repo contains code to conduct the human behavioral experiments reported in this paper, as well as analyze the resulting data from both human and modeling experiments. 

- `experiments`: This directory contains code to run the human behavioral experiments reported in this paper. 
- `analysis` (aka `notebooks`): This directory contains our analysis jupyter/Rmd notebooks. This repo assumes you have also imported model evaluation results from `physopt`. 
- `results`: This directory contains "intermediate" results of modeling/human experiments. It contains three subdirectories: `csv`, `plots`, and `summary`. 
	- `/results/csv/` contains `csv` files containing tidy dataframes with "raw" data. 
	- `/results/plots/` contains `.pdf`/`.png` plots, a selection of which are then polished and formatted for inclusion in the paper using Adobe Illustrator. 
	- *Important: Before pushing any csv files containing human behavioral data to a public code repository, triple check that this data is properly anonymized. This means no bare AMT Worker ID's or Prolific participant IDs.*
- `stimuli`: This directory contains any download/preprocessing scripts for data (a.k.a. stimuli) that are the _inputs_ to human behavioral experiments. This repo assumes you have generated stimuli using `tdw_physics`. This repo uses code in this directory to upload stimuli to AWS S3 and generate metadata to control the timeline of stimulus presentation in the human behavioral experiments.
- `utils`: This directory is meant to contain any files containing general helper functions. 

