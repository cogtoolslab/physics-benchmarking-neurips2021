## Analysis Directory Summary
#### This table covers 
- Content: what can this notebook generate (csv files, plots, etc.)
- Access: whether is only for internal use, or for public use
- Dependency: internal files that need to be executed before analysis notebook would be able to run

| File Name | Content | Access | Dependency 
| ------ | ------ | ------ | ------ |
analysis_helpers.py | - basic datafram info for import csv files<br> - functions defined to help load, clean, and caluclate statistics from the data | Public | - None
analyze_error_basic.ipynb | - display the video output of human experiment trials for each human error rate segment| Public | `./download_results.py`  `display_trials.py`
analyze_human_behavior_across_scenarios.ipynb | - Visualize distribution and compute summary statistics over human physical judgments across scenario | Public | `./download_results.py` 
analyze_human_behavior_single_scenario.ipynb | - Visualize distribution and compute summary statistics over human physical judgments for each scenario| Public | `./download_results.py`
analyze_human_model_behavior.ipynb | - analyse various statistics on subset of the whole data based on human-model accuracy comparison to study if any interesting relationsip exists| Public | `./download_results.py` `./summarize_human_model_behavior.ipynb` `./summarize_human_model_behavior_subset.ipynb`
analyze_model_model_behavior.ipynb | - analyse similarity of predictions made by different models | Public | `./download_results.py` `./summarize_human_model_behavior.ipynb`
check_metadata_for_matching_urls.ipynb | - helper that ensure that all urls match each other| Public | - None
demographics.ipynb | - providing interesting insights on demographic data exported from prolific | Public | `./download_results.py`
display_trials.py | - helper that provide visualization layout for trials video display | Public | - None
download_results.py | - used to download all needed human and training results in csv format for analysis | Public | - None
experiment_meta.py | - meta info on NeurIPS 21 experiment| Public | - None
familiariarization_exclusion.ipynb | - use to generate csv file on familiarization trials excluded| Public | `./download_results.py`
generate_dataframes.py | - get dataframes from mongoDB and saves them in the corresponding locations| Internal | - None
inference_human_model_behavior.html | - html file for inference_human_model_behavior notebook | Public | - None
inference_human_model_behavior.ipynb | - visualize human, model accuracy, human-human, model-human agreement (Cohen's kappa), and compare performance between models| Public | `./download_results.py` `./summarize_human_model_behavior.ipynb`
paper_plots.ipynb | - create plots that are in the paper | Public | `./download_results.py` `./summarize_human_model_behavior.ipynb`
requirements.txt | - dependency version requirement | Public | - None
stimulus_plots.ipynb | - plot pretty stimulus visual display | Public | `./download_results.py`
summarize_human_model_behavior.ipynb | - get distribution and compute summary statistics over human and model physical judgments <br> - output CSV that can be re-loaded into R notebook for statistical modeling & fancy visualizations| Public | `./download_results.py`
summarize_human_model_behavior_subset.ipynb | - doing the same thing as summarize_human_model_behavior.ipynb, but on certain subsets | Public | `./download_results.py`
upload_results.py | - upload results in the `result/csv` folder onto clound storage| Internal | - None

(Directory to contain analysis notebooks/scripts for this project.)
