# Physion: Evaluating Physical Prediction from Vision in Humans and Machines

![Animation of the 8 scenarios](figures/scenario_animation.gif)

This repo contains code and data to reproduce the results in our paper, [Physion: Evaluating Physical Prediction from Vision in Humans and Machines](https://arxiv.org/abs/2106.08261). Please see below for details about how to download the Physion dataset, replicate our modeling & human experiments, and statistical analyses to reproduce our results. 

1. [Downloading the Physion dataset](#downloading-the-physion-dataset)
2. [Dataset generation](#dataset-generation)
3. [Modeling experiments](#modeling-experiments)
4. [Human experiments](#human-experiments)
5. [Comparing models and humans](#comparing-models-and-humans)

-----

## Downloading the Physion dataset

### Downloading the **Physion test set** (a.k.a. stimuli)

#### PhysionTest-Core (270 MB)
`PhysionTest-Core` is all you need to evaluate humans and models on exactly the same test stimuli used in our paper. 

It contains eight directories, one for each scenario type (e.g., `collide`, `contain`, `dominoes`, `drape`, `drop`, `link`, `roll`, `support`).

Each of these directories contains three subdirectories:
- `maps`: Contains PNG segmentation maps for each test stimulus, indicating location of `agent` object in red and `patient` object in yellow. 
- `mp4s`: Contains the MP4 video files presented to human participants. The `agent` and `patient` objects appear in random colors. 
- `mp4s-redyellow`: Contains the MP4 video files passed into models. The `agent` and `patient` objects consistently appear in red and yellow, respectively.

**Download URL**: [https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Physion.zip](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Physion.zip).

#### PhysionTest-Complete (380 GB)
`PhysionTest-Complete` is what you want if you need more detailed metadata for each test stimulus. 

Each stimulus is encoded in an HDF5 file containing comprehensive information regarding depth, surface normals, optical flow, and segmentation maps associated with each frame of each trial, as well as other information about the physical states of objects at each time step. 

**Download URL**: [https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/PhysionTest.tar.gz](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/PhysionTest.tar.gz). 


You can also download the testing data for individual scenarios from the table in the next section.

### Downloading the **Physion training set**

#### Downloading `PhysionTrain-Training`

The dataset used to train the models we benchmarked consists of ~2000 movies from each of the eight physical scenarios (or subsets of this meant to assess various types of generalization.) These trials were generated from the same distribution of physical parameters as the testing stimuli (above), so models trained on this dataset will not encounter any "new physics" during testing.


#### Downloading `PhysionTrain-Readout`

In addition, we created "readout fitting sets" of 1000 trials for each of the eight scenarios. These trials are drawn from the same physical parameter distributions as above, but in addition they also have the same "red agent object, yellow patient object" visual appearance as the testing trials. The purpose of these readout sets is to fit a simple model (i.e. logistic regression) from a set of _pretrained model features_ to do the red-yellow OCP task. Code for using these readout sets to benchmark **any** pretrained model (not just models trained on the Physion training sets) will be released prior to publication.

You can download MP4s of all the training trials here [https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/PhysionTrainMP4s.tar.gz](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/PhysionTrainMP4s.tar.gz) and HDF5s for each scenario's training and readout sets below:

| Scenario | Training Set         | Readout Set       | Testing Set      |
| -------- | -------------------- | ----------------- | ---------------- |
| Dominoes | [Dominoes_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Dominoes_training_HDF5s.tar.gz) | [Dominoes_readout_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Dominoes_readout_HDF5s.tar.gz)         | [Dominoes_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Dominoes_testing_HDF5s.tar.gz) |
| Support | [Support_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Support_training_HDF5s.tar.gz) | [Support_readout_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Support_readout_HDF5s.tar.gz)         | [Support_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Support_testing_HDF5s.tar.gz) |
| Collide | [Collide_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Collide_training_HDF5s.tar.gz) | [Collide_readout_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Collide_readout_HDF5s.tar.gz)         | [Collide_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Collide_testing_HDF5s.tar.gz) |
| Contain | [Contain_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Contain_training_HDF5s.tar.gz) | [Contain_readout_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Contain_readout_HDF5s.tar.gz)         | [Contain_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Contain_testing_HDF5s.tar.gz) |
| Drop | [Drop_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drop_training_HDF5s.tar.gz) | [Drop_readout_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drop_readout_HDF5s.tar.gz)         | [Drop_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drop_testing_HDF5s.tar.gz) |
| Roll | [Roll_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Roll_training_HDF5s.tar.gz) | [Roll_readout_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Rollreadout_HDF5s.tar.gz)         | [Roll_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Roll_testing_HDF5s.tar.gz) |
| Link | [Link_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Link_training_HDF5s.tar.gz) | [Link_readout_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Link_readout_HDF5s.tar.gz)         | [Link_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Link_testing_HDF5s.tar.gz) |
| Drape | [Drape_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drape_training_HDF5s.tar.gz) | [Drape_readout_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drape_readout_HDF5s.tar.gz)         | [Drape_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drape_testing_HDF5s.tar.gz) |


## Dataset generation

This repo depends on outputs from [`tdw_physics`](https://github.com/neuroailab/tdw_physics).

Specifically, [`tdw_physics`](https://github.com/neuroailab/tdw_physics) is used to generate the dataset of physical scenarios (a.k.a. stimuli), including both the **training datasets** used to train physical-prediction models, as well as **test datasets** used to measure prediction accuracy in both physical-prediction models and human participants.

Instructions for using the ThreeDWorld simulator to regenerate datasets used in our work can be found [here](https://github.com/cogtoolslab/physics-benchmarking-neurips2021/tree/master/stimuli). Links for downloading the Physion testing, training, and readout fitting datasets can be found below.

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


## Comparing models and humans

The results reported in this paper can be reproduced by running the Jupyter notebooks contained in the `analysis` directory. 

1. **Downloading results.** To download the "raw" human and model prediction behavior, please navigate to the `analysis` directory and execute the following command at the command line: `python download_results.py`. This script will fetch several CSV files and download them to subdirectories within `results/csv`. If this does not work, please download this zipped folder (`csv`) and move it to the `results` directory: [https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/model_human_results.zip](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/model_human_results.zip).
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
