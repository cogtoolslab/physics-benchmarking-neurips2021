# Physion: Evaluating Physical Prediction from Vision in Humans and Machines

![Animation of the 8 scenarios](figures/scenario_animation.gif)

This repo contains code and data to reproduce the results in our NeurIPS 2021 paper, [Physion: Evaluating Physical Prediction from Vision in Humans and Machines](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/d09bf41544a3365a46c9077ebb5e35c3-Abstract-round1.html). For a brief overview, please check out our project website: [https://physion-benchmark.github.io/](https://physion-benchmark.github.io/). 

Please see below for details about how to download the Physion dataset, replicate our modeling & human experiments, and statistical analyses to reproduce our results.

1. [Downloading the Physion dataset](#downloading-the-physion-dataset)
2. [Dataset generation](#dataset-generation)
3. [Modeling experiments](#modeling-experiments)
4. [Human experiments](#human-experiments)
5. [Comparing models and humans](#comparing-models-and-humans)

-----

## Downloading the Physion dataset

### Downloading the **Physion test set** (a.k.a. stimuli)

All videos in the Physion test set have been manually evaluated to ensure that the behavior of the simulated physics does not feature glitches or unexpected behaviors. A small number of stimuli that contain potential physics glitches have been identified; the stimulus names can be seen [here](analysis/manual_stim_evaluation_buggy_stims.txt) or downloaded at the following link:

**Download URL**: [https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/manual_stim_evaluation_glitchy_test_stims.txt](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/manual_stim_evaluation_glitchy_test_stims.txt).

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

**Download URL**: [https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/PhysionTestHDF5.tar.gz](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/PhysionTestHDF5.tar.gz). 

You can also download the testing data for individual scenarios from the table in the next section.

### Downloading the **Physion training set**

#### Downloading `PhysionTrain-Dynamics`

`PhysionTrain-Dynamics` contains the full dataset used to train the dynamics module of models benchmarked in our paper. It consists of approximately 2K stimuli per scenario type.

**Download URL** (770 MB): [https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/PhysionTrainMP4s.tar.gz](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/PhysionTrainMP4s.tar.gz)

#### Downloading `PhysionTrain-Readout`

`PhysionTrain-Readout` contains a separate dataset used for training the object-contact prediction (OCP) module for models pretrained on the `PhysionTrain-Dynamics` dataset. It consists of 1K stimuli per scenario type.

The `agent` and `patient` objects in each of these readout stimuli consistently appear in red and yellow, respectively (as in the `mp4s-redyellow` examples from `PhysionTest-Core` above).

*NB*: Code for using these readout sets to benchmark **any** pretrained model (not just models trained on the Physion training sets) will be released prior to publication.

**Download URLs** for complete `PhysionTrain-Dynamics` and `PhysionTrain-Readout`:

| Scenario | Dynamics Training Set         | Readout Training Set       | Test Set      |
| -------- | -------------------- | ----------------- | ---------------- |
| Dominoes | [Dominoes_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Dominoes_dynamics_training_HDF5s.tar.gz) | [Dominoes_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Dominoes_readout_training_HDF5s.tar.gz)         | [Dominoes_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Dominoes_testing_HDF5s.tar.gz) |
| Support | [Support_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Support_dynamics_training_HDF5s.tar.gz) | [Support_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Support_readout_training_HDF5s.tar.gz)         | [Support_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Support_testing_HDF5s.tar.gz) |
| Collide | [Collide_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Collide_dynamics_training_HDF5s.tar.gz) | [Collide_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Collide_readout_training_HDF5s.tar.gz)         | [Collide_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Collide_testing_HDF5s.tar.gz) |
| Contain | [Contain_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Contain_dynamics_training_HDF5s.tar.gz) | [Contain_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Contain_readout_training_HDF5s.tar.gz)         | [Contain_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Contain_testing_HDF5s.tar.gz) |
| Drop | [Drop_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drop_dynamics_training_HDF5s.tar.gz) | [Drop_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drop_readout_training_HDF5s.tar.gz)         | [Drop_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drop_testing_HDF5s.tar.gz) |
| Roll | [Roll_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Roll_dynamics_training_HDF5s.tar.gz) | [Roll_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Rollreadout_HDF5s.tar.gz)         | [Roll_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Roll_testing_HDF5s.tar.gz) |
| Link | [Link_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Link_dynamics_training_HDF5s.tar.gz) | [Link_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Link_readout_training_HDF5s.tar.gz)         | [Link_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Link_testing_HDF5s.tar.gz) |
| Drape | [Drape_dynamics_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drape_dynamics_training_HDF5s.tar.gz) | [Drape_readout_training_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drape_readout_training_HDF5s.tar.gz)         | [Drape_testing_HDF5s](https://physics-benchmarking-neurips2021-dataset.s3.amazonaws.com/Drape_testing_HDF5s.tar.gz) |


## Dataset generation

This repo depends on outputs from [`tdw_physics`](https://github.com/neuroailab/tdw_physics).

Specifically, [`tdw_physics`](https://github.com/neuroailab/tdw_physics) is used to generate the dataset of physical scenarios (a.k.a. stimuli), including both the **training datasets** used to train physical-prediction models, as well as **test datasets** used to measure prediction accuracy in both physical-prediction models and human participants.

Instructions for using the ThreeDWorld simulator to regenerate datasets used in our work can be found [here](https://github.com/cogtoolslab/physics-benchmarking-neurips2021/tree/master/stimuli/generation). Links for downloading the Physion testing, training, and readout fitting datasets can be found [here](https://github.com/cogtoolslab/physics-benchmarking-neurips2021/tree/controllers/stimuli/generation).

## Modeling experiments

<!-- **TODO**: Add topic sentence that states high-level input-output relationship between physopt and current repo. -->

The modeling component of this repo depends on the [`physopt`](https://github.com/neuroailab/physopt-physics-benchmarking) repo.  The [`physopt`](https://github.com/neuroailab/physopt-physics-benchmarking) repo implements an interface through which a wide variety of physics prediction models from the literature (be they neural networks or otherwise) can be adapted to accept the inputs provided by our training and testing datasets and produce outputs for comparison with our human measurements. 


The [`physopt`](https://github.com/neuroailab/physopt-physics-benchmarking) also contains code for model training and evaluation.  Specifically, [`physopt`](https://github.com/neuroailab/physopt-physics-benchmarking) implements three train/test procols:

- The `only protocol`, in which each candidate physics model architecture is trained -- using that model's native loss function as specified by the model's authors -- separately on each of the scenarios listed above (e.g. "dominoes", "support", &c).  This produces eight separately-trained models per candidate architecture (one for each scenario).  Each of these separate models are then tested in comparison to humans on the testing data for that scenario.
- A `all protocol`, in which each candidate physics architecture is trained on mixed data from all of the scenarios simultaneously (again, using that model's native loss function). This single model is then tested and compared to humans separately on each scenario.
- A `all-but-one protocol`, in which each candidate physics architecture is trained on mixed data drawn for all but one scenario -- separately for all possible choices of the held-out scenario.  This produces eight separately-trained models per candidate architecture (one for each held-out scenario).  Each of these separate models are then tested in comparison to humans on the testing data for that scenario.

Results from each of the three protocols are separately compared to humans (as described below in the section on comparison of humans to models).  All model-human comparisons are carried using a representation-learning paradigm, in which models are trained on their native loss functions (as encoded by the original authors of the model).  Trained models are then evaluated on the specific physion red-object-contacts-yellow-zone prediction task.  This evaluation is carried by further training a "readout", implemented as a linear logistic regression.  Readouts are always trained in a per-scenario fashion. 

Currently, physopt implements the following specific physics prediction models:


| Model Name | Our Code Link | Original Paper | Description |
| ---------- | ------------- | -------------- | ----------- |
| SVG        |               | [`Denton and Fergus 2018`](http://proceedings.mlr.press/v80/denton18a.html) | Image-like latent |
| OP3        |               | [`Veerapaneni et. al. 2020`](http://proceedings.mlr.press/v100/veerapaneni20a.html) | |
| CSWM       |               | [`Kipf et. al. 2020`](https://openreview.net/forum?id=H1gax6VtDB) | |
| RPIN       |               | [`Qi et. al. 2021`](https://openreview.net/forum?id=_X_4Akcd8Re) | |
| pVGG-mlp   |               | | |
| pVGG-lstm  |               | | |
| pDEIT-mlp  |               | [`Touvron et. al. 2020`](https://arxiv.org/abs/2012.12877)| |
| pDEIT-lstm |               | | |
| GNS        |               | [`Sanchez-Gonzalez et. al. 2020`](https://arxiv.org/abs/2002.09405)| |
| GNS-R      |               | | |
| DPI        |               | [`Li et. al. 2019`](http://dpi.csail.mit.edu/)| |  


## Human experiments

This repo contains code to conduct the human behavioral experiments reported in this paper, as well as analyze the resulting data from both human and modeling experiments. 

The details of the experimental design and analysis plan are documented in our [study preregistration](https://github.com/cogtoolslab/physics-benchmarking-neurips2021/blob/master/prereg/preregistration_neurips2021.md) contained within this repository. The format for this preregistration is adapted from the templates provided by the Open Science Framework for our studies, and put under the same type of version control as the rest of the codebase for this project. 

Here is what each main directory in this repo contains:
- `experiments`: This directory contains code to run the online human behavioral experiments reported in this paper. More detailed documentation of this code can be found in the [README](https://github.com/cogtoolslab/physics-benchmarking-neurips2021/blob/master/experiments/README.md) file nested within the [`experiments` subdirectory](https://github.com/cogtoolslab/physics-benchmarking-neurips2021/tree/master/experiments).
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
