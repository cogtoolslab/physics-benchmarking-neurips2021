### Key components we need to mock up a single working trial of evalTower

1. `index.html`: HTML file that we can open in our web browser locally
2. `js/jspsych.js`: core jsPsych library 
3. `js/setup.js`: constructs trial timeline
4. `js/jspsych-image-button-response.js`: custom plugin that will display: (i) reference tower image, (ii) likert scale
5. `data/example.json`: a single trial's worth of data that can be loaded in to prototype the plugin
Tip: Include this line in the header of your `index.html` file, and then you will see that your data is a global variable now: 
`<script src="data/example.json"></script>`
6. `jspsych.css`: core jsPsych CSS stylesheet


### Study Iterations:
#### "Testing-new-meta" (~11/30/2020) 
 - This version has an updated metadata file. It imports all of the trials as one meta object and then shuffles them.
 - Currently 72 trials (69 curiodrop towers and 3 catch trials)
 - Two possible conditions: "stable" and "interesting", we use same stimuli for both
 
#### "run_0" (~1/13/2021)
dbname = 'curiotower';
colname = 'tdw-height3Jitter3';
iterationName = 'run_0'
(app.js colname = 'curiotower')

N=100 on 1/14/2021
 - This version uses our 3x3 design for tdw towers. 
    - We vary the x_jitter(low = 0, med = 0.07, high = 0.1) and num_blocks (2,4,8).
    - We also take two viewpoints (from above and below)
    - Each tower set is generated from 8 different seeds, yields 8x3x3x2=144 stimuli
 - We also have two catch trials that are just a single block, generated with seed 999
 - As before, we are testing the stability and interestingness conditions


#### "run_1" (~1/30/2021)
dbname = 'curiotower';
colname = 'curiodrop';
iterationName = 'run_1'
(app.js colname = 'curiotower_curiodrop')

N=20 on 1/30/2021
 - We ran another 25 subjects on the cooltower stimuli (same 72 trials and catches as the "testing-new-meta" iteration)
