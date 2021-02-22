# human-physics-benchmarking

- `analysis` (aka `notebooks`): This directory contains jupyter/Rmd notebooks for exploratory code development and data analysis.
- `experiments`: This directory contains code to run online behavioral experiments. 
- `results`: This directory is meant to contain "intermediate" results of your computational/behavioral experiments. It should minimally contain two subdirectories: `csv` and `plots`. So `/results/csv/` is the path to use when saving out `csv` files containing tidy dataframes. And `/results/plots/` is the path to use when saving out `.pdf`/`.png` plots, a small number of which may be then polished and formatted for figures in a publication. *Important: Before pushing any csv files containing human behavioral data to a public code repository, triple check that this data is properly anonymized. This means no bare AMT Worker ID's.*
- `stimuli`: This directory is meant to contain any download/preprocessing scripts for data that are _inputs_ to this project. For many projects, these will be images. This is also where you want to place any scripts that will upload your data to our `stimuli`  MongoDB database and any image data to Amazon S3 (so that it has a semi-permanent URL you can use to insert into your web experiment.)
- `utils`: This directory is meant to contain any files containing general helper functions. 
