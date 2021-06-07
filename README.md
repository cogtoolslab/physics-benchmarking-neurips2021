# Physion: Evaluating Physical Prediction from Vision in Humans and Machines

## Dataset generation

This repo depends on outputs from [`tdw_physics`](https://github.com/threedworld-mit/tdw).

Specifically, [`tdw_physics`](https://github.com/threedworld-mit/tdw) is used to generate the dataset of physical scenarios (a.k.a. stimuli), including both the **training datasets** used to train physical-prediction models, as well as **test datasets** used to measure prediction accuracy in both physical-prediction models and human participants.

## Modeling experiments
This repo depends on outputs from [`physopt`](https://github.com/neuroailab/physopt-physics-benchmarking).

The [`physopt`](https://github.com/neuroailab/physopt-physics-benchmarking) repo was used to conduct physical-prediction model training and evaluation. 

## Human experiments

This repo contains code to conduct the human behavioral experiments reported in this paper, as well as analyze the resulting data from both human and modeling experiments. 

Here is what each main directory in this repo contains:
- `experiments`: This directory contains code to run the online human behavioral experiments reported in this paper. 
- `analysis` (aka `notebooks`): This directory contains our analysis jupyter/Rmd notebooks. This repo assumes you have also imported model evaluation results from `physopt`. 
- `results`: This directory contains "intermediate" results of modeling/human experiments. It contains three subdirectories: `csv`, `plots`, and `summary`. 
	- `/results/csv/` contains `csv` files containing tidy dataframes with "raw" data. 
	- `/results/plots/` contains `.pdf`/`.png` plots, a selection of which are then polished and formatted for inclusion in the paper using Adobe Illustrator. 
	- *Important: Before pushing any csv files containing human behavioral data to a public code repository, triple check that this data is properly anonymized. This means no bare AMT Worker ID's or Prolific participant IDs.*
- `stimuli`: This directory contains any download/preprocessing scripts for data (a.k.a. stimuli) that are the _inputs_ to human behavioral experiments. This repo assumes you have generated stimuli using `tdw_physics`. This repo uses code in this directory to upload stimuli to AWS S3 and generate metadata to control the timeline of stimulus presentation in the human behavioral experiments.
- `utils`: This directory is meant to contain any files containing general helper functions. 

## Reproducibility of results

### Regenerating the dataset
To download the code used to generate the training and test datasets, please follow these instructions:
1. XXX
2. YYY
3. ZZZ

### Reproducing modeling experiments
To reproduce the model training and evaluation experiments, please follow these instructions:
1. XXX
2. YYY
3. ZZZ

### Reproducing human experiments
To reproduce the human behavioral experiments, please follow these instructions:
1. XXX
2. YYY
3. ZZZ

### Reproducing the analyses of human and modeling behavior reported in the paper

The results reported in this paper can be reproduced by running the Jupyter notebooks contained in the `analysis` directory. 

1. **Downloading results.** To download the "raw" human and model prediction behavior, please navigate to the `analysis` directory and execute the following command at the command line: `python download_results.py`. This script will fetch several CSV files and download them to subdirectories within `results/csv`. If this does not work, please download this zipped folder: [https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/model_human_results.zip](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/model_human_results.zip).
2. **Reproducing analyses.** To reproduce the key analyses reported in the paper, please run the following notebooks in this sequence:
	- `summarize_human_model_behavior.ipynb`: The purpose of this notebook is to:
		* Apply preprocessing to human behavioral data
		* Visualize distribution and compute summary statistics over **human** physical judgments
		* Visualize distribution and compute summary statistics over **model** physical judgments
		* Conduct human-model comparisons
		* Output summary CSVs that can be used for further statistical modeling & create publication-quality visualizations
	- `inference_human_model_behavior.ipynb`: The purpose of this notebook is to: 
		* Visualize human and model prediction accuracy (proportion correct)
		* Visualize average-human and model agreement (RMSE)
		* Visualize human-human and model-human agreement (Cohen's kappa)
		* Compare performance between models	
	- `paper_plots.ipynb`: The purpose of this notebook is to create publication-quality figures for inclusion in the paper.









