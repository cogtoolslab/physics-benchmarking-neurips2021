# Pregistration

**Researchers**: 
<!-- Not actually sure who everyone on the project actually is -->

## Study information
<!-- give your study a brief and informative title -->
**Title**: Human physics benchmarking

### Research questions
<!-- specify the broad and specific questions guiding your study -->
Predicting the future outcome of physical scenarios is a paradigm case of using models to represent and reason about the world. Intuitive physics is central to intelligent behavior in physical environments. 
In this study, we aim to identify features of physical scenes that make correct human physical prediction difficult. 
Additionally, we aim to collect data on which scenes are difficult for human subjects to predict correctly in order to compare human subjects against a range of computational models of physical scene prediction. 

### Hypotheses
<!-- list 2 specific, concise, and testable hypotheses, including the if-then logic statements for your predictions. -->
We predict that scenes which (1) contain more elements, (2) contain distractor elements and (3) contains occluder elements are harder to correctly predict for human subjects. 
Additionally (4), we predict that scenes that lead to more incorrect predictions also tend to have a longer reaction time (ie. people take longer to come up with an answer to difficult scenes).

<!-- Also: camera angle, jitter, percent of target visible (_id map) -->
 
## Design Plan
###   Study type
 <!-- indicate whether your study will be experimental or correlational -->
 Experimental
###   Study design: stimulus generation
 <!-- describe the overall design of the study (what will be manipulated and/or measured, specify whether manipulations will be between- or within-subjects, etc.) -->
 Within-subjects design. All subjects will be shown XXX scenes drawn from a set in random order.
 
 `TODO: describe sampling procedure over these stim dimensions.`
 The scenes in the set vary along the following dimensions:
 * Background type - `TODO: specify levels`
 * Number of physical elements ("dominoes") - `TODO: specify levels` 
 * Number and kind of distractor objects (which are shown behind the physical elements) - `TODO: specify levels` 
 * Number and kind of occluder objects (shown in front of and partially covering the physical objects) - `TODO: specify levels` 
 * Color of the physical objects - `TODO: specify levels` 
 * Positional jitter of the physical objects - `TODO: specify levels` 
 * Rotational jitter of the physical objects - `TODO: specify levels`

Example stimulus:\
![Example stimulus](.preregistration_dominoes_pilot/pic_1615209831541.png)  

###   Study design: task procedure
`TODO: Perhaps lay out in a numbered list the full sequence of events that transpire, in order within a session.`

`TODO: Describe comprehension check trials where the participant demonstrates that they are able to reliably DETECT the target event. Foreshadowing/anticipating that we will need to specify reasonable criteria for what we do with outlier sessions where participants truly struggle with these.`

 Each stimulus consists of a short video of a row of "dominoes" (physical objects), where the first domino is toppled by applying a force and the last one ("target object", colored red) is placed in front of a yellow target area. The video end after 1500ms, so whether or not the target object falls on the target area is not shown. 
 Subjects are tasked with responding "yes" or "no" depending on whether they'll be predict that the target object will hit the target area in the remainder of the video (not shown). No feedback during trials is given.

 Each trial is preceded by a fixation cross shown for a time randomly sampled from the interval $[500,1500]$ ms. After $1500$ms, the video is removed and the white background is shown in its place (so subjects need to rely on the information they were able to gather in the $1500$ms to make their prediction). The next trial is started immediately after giving a response. 
 To account for side biases, the order of response button is randomized between subjects

 Before trials begin, subjects are shown 5 familiarization trials. After making a prediction, they are informed whether the prediction was correct and is shown the unabridged stimulus including the result of the trial. 

 Stimuli are designed to provide a roughly 50/50 split between positive and negative trials ("does the target object hit the target area?") in the set, with not counterbalancing on the sample shown to participants. `TODO: 0. Re-factor so that this information is contained above with the other stimulus sampling info. 1. In generate_metadata notebook, curate dataset so that it is balanced over stim dimensions. 2. Pre-sample sessions that ensure that exactly 50% of trials are positive, and potentially (at least approx.) balanced over a subset of the other dimensions.`

 After the trials, subjects will be asked to provide:
 * age
 * gender
 * education level
 * difficulty rating
 * one trial Shephard Metzler mental rotation task (`TODO: keep in the experiment? either investigate how many of these items would we need to ensure measurement reliability or defer to think about how to incorporate other classic spatial-cognition tests in the future to estimate within-subject between-task covariation.`)
 * free form feedback on the task

 After the end of the study, subjects will be told their overall accuracy and the corresponding percentile compared to other subjects on the study. 

## Sampling Plan
###   Data collection procedure
 <!-- describe the method you will use to collect your data, and your inclusion/exclusion criteria. This should include your sampling frame, how participants will be recruited, and whether/how they will be compensated. -->
Participants will be recruited from {Prolific/Amazon Mechnical Turk/SONA/XXX} and compensated $XXX, which roughly corresponds to $XXX/hr. TODO MAYBE: Additionally, subjects will be rewarded for correct predictions. 

Subjects are only allowed to take the task once.

###   Sample size
 <!-- indicate your target sample size and why that is your target (might be based in past research, for example) -->
 We aim for a sample size of XXX subjects based on prior experience on the task.

###   Stopping rule
 <!-- specify how you will determine when to stop data collection -->
 Data collection will be stopped after the planned number of subjects has been recorded. 

## Variables
###   Manipulated variables
 <!-- If applicable, precisely define any variables you plan to manipulate, including the levels and whether the manipulation will be between or within subjects. -->
As outlined above, subjects are not assigned to any conditions. The manipulations consist of the stimuli with underlying parameters as well as the sampling of stimuli.

###   Measured variables
 <!-- Precisely define each variable that you will measure. This includes outcome measures, as well as other measured predictor variables. -->
We measure:
* `response`: prediction (either yes/no)
* `rt`: time taken to make prediction

###   Indices
 <!-- If applicable, define how measures will be combined into an index (or even a mean) and what measures will be used. Include a formula or a precise description of the method. -->
 *Not applicable*

## Analysis Plan
###   Data exclusion
 <!-- How will you determine which data points or samples (if any) to exclude from your analyses? How will outliers be handled? Will you use any awareness or attention check? -->
 No explicit awareness check will be performed. 
 Subjects will be excluded if they display a sequence of responses clearly not related to the actual stimuli shown, precisely a sequence that:
 * contains XXX consecutive "yes" or "no" answers
 or
 * contains a sequence of at least XXX iterating "yes" or "no"

###   Missing data
 Trials with missing data (ie. if a subjects stop mid-way through) will be discarded.

<!-- Or should we keep them, since we're mostly interested on stimuli ratings? -->

###   Planned visualization
 <!-- Describe what kind of visualization you would use (e.g. boxplot, faceted histogram, scatterplot, etc.) to evaluate your data and determine what it can tell you about your research question -->
A scatter plot, in which the points correspond to individual stimuli. The x-axis represents the number of physical objects in the stimulus (with jitter applied as the measure is ordinal), the y-axis represents the percentage of correct predictions out of all predictions for that stimulus. 
Points are colorized according to the presence of distractor objects and the symbol representing the point denotes the presence or absence of occluder objects.

Additionally, marginal bar plots showing rate of correct prediction for stimuli according to (1) number of physical objects, (2) presence of distractor and (3) presence of occluder are shown.

To investigate reaction time as a function of rate of correct predictions, we show a scatter plot in which the x-axis represents the rate of correct predictions and the y-axis the mean reaction time (with confidence intervals shown). The points correspond to individual stimuli. A fit line is shown.

###   Predicted results
 <!-- What pattern do you expect to see in your planned visualization, based on the hypotheses you described earlier? -->
 We expect to see a monotonic decrease in perfect predictions with increased number of objects. Likewise, we expect the presence of distractor and occluder objects to lead to a lower rate of perfect reconstructions. 

 We also expect that the harder a stimulus is to predict correctly, the longer subjects take to make a response.

###   Exploratory analysis
 <!-- If you plan to explore your data to look for unspecified differences or relationships, you may include those plans here. If you list an exploratory test here, you are not obligated to report its results, but you are obligated to describe it as an exploratory result. -->
We aim to explore the relation of demographic variables as well as the result of a one-trial spatial reasoning task on the performance of subjects: how does age, gender, educational status and the the result of a one-trial spatial reasoning task relate to the overall accuracy of a subject?

Additionally, we aim to explore whether subjects show a consistent bias towards towards positive/negative predictions. 

<!-- We might also explore whether the speed of response predicts its correctness. Curve might be inverted U-shape: too fast or too slow leads to bad predictions. Perhaps too fast not, since the subjects always get 1500ms -->
