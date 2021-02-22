# Project Template

This is an example of how a cogtoolslab project repo should be organized.

It contains several subdirectories that will contain standard elements of almost every project:

- `analysis` (aka `notebooks`): This directory will typically contain jupyter/Rmd notebooks for exploratory code development and data analysis.
- `experiments`: If this is a project that will involve collecting human behavioral data, this is where you want to put your experimental code. If this is a project that will involve evaluation of a computational model's behavior on a task, this is also where you want to put the task code.
- `model`: If this is a cognitive modeling project, this is where you want to put your model definitions. If this project involves training neural networks, you might consider starting out putting training scripts in here, but then splitting these off into a separate `training` dir. 
- `results`: This directory is meant to contain "intermediate" results of your computational/behavioral experiments. It should minimally contain two subdirectories: `csv` and `plots`. So `/results/csv/` is the path to use when saving out `csv` files containing tidy dataframes. And `/results/plots/` is the path to use when saving out `.pdf`/`.png` plots, a small number of which may be then polished and formatted for figures in a publication. *Important: Before pushing any csv files containing human behavioral data to a public code repository, triple check that this data is properly anonymized. This means no bare AMT Worker ID's.*
- `stimuli`: This directory is meant to contain any download/preprocessing scripts for data that are _inputs_ to this project. For many projects, these will be images. This is also where you want to place any scripts that will upload your data to our `stimuli`  MongoDB database and any image data to Amazon S3 (so that it has a semi-permanent URL you can use to insert into your web experiment.)
- `utils`: This directory is meant to contain any files containing helper functions. 

### For general handy computing tips, please see the [`handy_tips` repo](https://github.com/cogtoolslab/handy_tips).

### Note about other project documentation 

#### Starter Google Doc

When we spin up a new project, the first thing we'll often do to collect our thoughts is create a Google Doc. This is b/c this file format is easy to share and flexible in format. This google doc is also where you should take notes during our meetings, and collect high-level TODO items, especially those that are not immediately actionable in code. .For code development TODO's, we will often instead use GitHub Issues.

#### Open Science Framework for pre-registration of behavioral experiments

Once we are in the later stages of desigining a new human behavioral experiment and preparing to run our first pilot, we will write up a pre-registration and post it to the [Open Science Framework](https://osf.io/). We subscribe to the philosophy that "pre-registrations are a plan, not a prison." They help us transparently document our thinking and decision-making process both for ourselves and for others, and will help us distinguish between confirmatory and exploratory findings. We do not believe that there is a single best way to write a pre-registration, but in many cases a more detailed plan will help us to clarify our experimental logic and set up our analyses accordingly (i.e., what each hypothesis predicts, which measures and analyses we will use to evaluate each relevant hypothesis). 

#### Manuscripts (including conference papers/abstracts) 

When we are preparing to write up a manuscript (or a conference paper), we will create a new repo, usually following the convention: `projectname_latex`. This is where you will want to place your LaTeX source `.tex` files for your paper and your publication-ready figures as high-resolution `.pdf` files in the `figures` directory. We typically format and fine-tune our figures using Adobe Illustrator.
