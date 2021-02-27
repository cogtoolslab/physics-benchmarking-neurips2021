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
#### Pilot
