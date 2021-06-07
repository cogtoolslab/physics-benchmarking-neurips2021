# human-physics-benchmarking

## Dependencies

This repo depends on outputs from [`tdw_physics`](https://github.com/threedworld-mit/tdw) and [`physopt`](https://github.com/neuroailab/physopt-physics-benchmarking).


## Repo organization

- `analysis` (aka `notebooks`): This directory contains our analysis jupyter/Rmd notebooks. This repo assumes you have also imported model evaluation results from `physopt`. 
- `experiments`: This directory contains code to run online behavioral experiments. 
- `results`: This directory is meant to contain "intermediate" results of your computational/behavioral experiments. It should minimally contain two subdirectories: `csv` and `plots`. So `/results/csv/` is the path to use when saving out `csv` files containing tidy dataframes. And `/results/plots/` is the path to use when saving out `.pdf`/`.png` plots, a small number of which may be then polished and formatted for figures in a publication. *Important: Before pushing any csv files containing human behavioral data to a public code repository, triple check that this data is properly anonymized. This means no bare AMT Worker ID's.*
- `stimuli`: This directory is meant to contain any download/preprocessing scripts for data that are _inputs_ to this project. This repo assumes you have generated stimuli using `tdw_physics`. 
- `utils`: This directory is meant to contain any files containing general helper functions. 
