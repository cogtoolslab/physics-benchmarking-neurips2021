var DEBUG_MODE = false; //print debug and piloting information to the console

function sendData(data) {
  console.log('sending data to mturk');
  jsPsych.turk.submitToTurk({
    'score': 0 //this is a dummy placeholder
  });
}

//randomize button order on a subject basis
var get_random_choices = () => {if(Math.random() > .5){return ["NO", "YES"];}else{return ["YES", "NO"];}};
var choices = get_random_choices(); //randomize button order

// Set the important study info here
var dbname = 'human_physics_benchmarking'; //insert DATABASE NAME
var colname = 'containment_pilot'; //insert COLLECTION NAME
var itname = 'production_1_testing'; //insert ITERATION NAME. This marks the responses, but does NOT determine which stimuli are pulled. Change the field in app.js for that

// Define trial object with boilerplate
function Experiment() {
  this.type = 'video-overlay-button-response',
  this.dbname = dbname;
  this.colname = colname;
  this.iterationName = itname;
  this.response_allowed_while_playing = false;
  // this.phase = 'experiment';
  this.condition = 'prediction';
  this.prompt = 'Is the red object going to hit the yellow area?';
  this.choices = choices;
};

function FamiliarizationExperiment() {
  // extends Experiment to provide basis for familizarization trials
  Experiment.call(this);
  this.condition = 'familiarization_prediction';
  // this.phase = 'familiarization';
}

var last_correct = undefined;  //was the last trial correct? Needed for feedback in familiarization
var correct = 0;
var total = 0;
var last_yes = undefined;

function setupGame() {
  socket.on('onConnected', function (d) {

    var queryString = window.location.search;
    var urlParams = new URLSearchParams(queryString);
    var prolificID = urlParams.get('PROLIFIC_PID')   // ID unique to the participant
    var studyID = urlParams.get('STUDY_ID')          // ID unique to the study
    var sessionID = urlParams.get('SESSION_ID')      // ID unique to the particular submission
    // Get workerId, etc. from URL (so that it can be sent to the server)
    //var turkInfo = jsPsych.turk.turkInfo();

    // These are flags to control which trial types are included in the experiment
    const includeIntro = true;
    const includeSurvey = true;
    const includeMentalRotation = false;
    const includeGoodbye = true;
    const includeFamiliarizationTrials = true;

    var gameid = d.gameid;
    var stims = d.stims
    var familiarization_stims = d.familiarization_stims
    if(DEBUG_MODE){
      console.log('gameid', gameid);    
      console.log('stims', stims);    
      console.log('familiarization_stims', familiarization_stims);
    }    
      
    // at end of each trial save data locally and send data to server
    var main_on_finish = function (data) {
      // let's add gameID and relevant database fields
      data.gameID = gameid;
      data.dbname = dbname;
      data.colname = colname;
      data.iterationName = itname;
      if(DEBUG_MODE){
        socket.emit('currentData', data);
        console.log('emitting data',data);
    }
    }

    // at end of each trial save data locally and send data to server
    var stim_on_finish = function (data) {
      // let's add gameID and relevant database fields
      data.gameID = gameid;
      data.dbname = dbname;
      data.colname = colname;
      data.iterationName = itname;
      data.stims_not_preloaded = /^((?!chrome|android).)*safari/i.test(navigator.userAgent); //HACK turned off preloading stimuli for Safari in jspsych-video-button-response.js
      jsPsych.data.addProperties(jsPsych.currentTrial()
      ); //let's make sure to send ALL the data //TODO: maybe selectively send data to db
      // lets also add correctness info to data
      data.correct = data.target_hit_zone_label == (data.response == "YES");
      if(data.correct){correct+=1};
      total += 1;
      if(DEBUG_MODE){
        if(data.correct){
          console.log("Correct, got ",_.round((correct/total)*100,2),"% correct")}
          else{
            console.log("Wrong, got ",_.round((correct/total)*100,2),"% correct")
          };
        }
      last_correct = data.correct; //store the last correct for familiarization trials
      last_yes = (data.response == "YES"); //store if the last reponse is yes
      socket.emit('currentData', data);
      if(DEBUG_MODE){console.log('emitting data',data);}
    }

    var stim_log = function(data){
      if(DEBUG_MODE){
        console.log("This is " + data.stim_ID + " with label " + data.target_hit_zone_label);
      }
    }
    
    // Now construct trials list    
    var experimentInstance = new Experiment;
    var familiarizationExperimentInstance = new FamiliarizationExperiment;
    
    var fixation = { // per https://stackoverflow.com/questions/35826810/fixation-cross-in-jspsych
      type: 'html-keyboard-response',
      stimulus: '<div style="font-size:60px">+</div>',
      choices: jsPsych.NO_KEYS,
      // trial_duration: 1000, // in ms
      on_start: (trial) => {
        trial.trial_duration = Math.random() * 1000 + 500 //random duration in milliseconds
      },
      post_trial_gap: 0,
      on_finish: ()=>{} // do nothing on trial end
    }; 
    
    // set up familiarization trials
    var familiarization_trials_pre =  _.map(familiarization_stims, function(n,i) {
      return _.extend({}, familiarizationExperimentInstance, n, {
        trialNum: i,
        stimulus: [n.stim_url],
        overlay: [n.map_url],
        overlay_time: 2.,
        blink_time: 500,
        stop: 1.5, //STIM DURATION stop the video after X seconds
        width: 500,
        height: 500,
        post_trial_gap: 0,
        on_start: stim_log,
        on_finish: stim_on_finish,
        prolificID:  prolificID,
        studyID: studyID, 
        sessionID: sessionID,
        gameID: gameid,
        target_hit_zone_label: n.target_hit_zone_label,
        stim_ID: n.stim_ID
        // save_trial_parameters: {} //selectively save parameters
      });
    });

    var familiarization_trials_post =  _.map(familiarization_stims, function(n,i) {
      return _.extend({}, familiarizationExperimentInstance, n, {
        trialNum: i,
        stimulus: [n.stim_url], //rename stim_url for the video plugin
        // stop: 1.5, //STIM DURATION stop the video after X seconds
        response_allowed_while_playing: false,
        width: 500,
        height: 500,
        post_trial_gap: 0,
        on_finish: () => {}, //do nothing after trial shown
        prolificID:  prolificID,
        studyID: studyID, 
        sessionID: sessionID,
        gameID: gameid,
        target_hit_zone_label: n.target_hit_zone_label,
        stim_ID: n.stim_ID,
        choices: ["Next"],
        prompt: () => {
          if(last_correct & last_yes) {
            return "✅ Nice, you got that right. The red object did indeed hit the yellow area. Above, you see the full video.";
          } 
          else if (last_correct & !last_yes) {
            return "✅ Nice, you got that right. The red object indeed did not hit the yellow area. Above, you see the full video.";
          } 
          else if (!last_correct & last_yes) {
            return "❌ Sorry, you got that one wrong. The red object did not hit the yellow area. Above, you see the full video.";
          } 
          else {
            return "❌ Sorry, you got that one wrong. The red object did hit the yellow area. Above, you see the full video.";
          }}
        // save_trial_parameters: {} //selectively save parameters
      });
    });

    var end_familiarization = {
      type: 'instructions',
      pages: [
        'You\'re now ready to start the full experiment.',
      ],
      show_clickable_nav: true,
      allow_backward: false,
      delay: false,
      on_finish: () => {
        correct = 0;
        total = 0; //reset the counters for the console feedback
      }
    };

    familiarization_trials = _.flatten(_.zip(familiarization_trials_pre,familiarization_trials_post));
    familiarization_trials.push(end_familiarization);
    
    // Variables shared for all trials. Set up the important stuff here.
    var trials = _.map(stims, function(n,i) {
      return _.extend({}, experimentInstance, n, {
        trialNum: i,
        stimulus: [n.stim_url],
        overlay: [n.map_url],
        overlay_time: 2.,
        blink_time: 500,
        stimulus_metadata: n, //to dump all the metadata back to mongodb
        stop: 1.5, //STIM DURATION stop the video after X seconds
        width: 500,
        height: 500,
        post_trial_gap: 0,
        on_start: stim_log,
        on_finish: stim_on_finish,
        prolificID:  prolificID,
        studyID: studyID, 
        sessionID: sessionID,
        gameID: gameid,
        target_hit_zone_label: n.target_hit_zone_label,
        stim_ID: n.stim_ID
        // save_trial_parameters: {} //selectively save parameters
      });
    });

    //add fixation crosses
    trials = _.flatten(_.zip(_.fill(Array(trials.length),fixation), trials));
    if(DEBUG_MODE){
      console.log('experiment trials', trials);
      console.log('familiarization trials', familiarization_trials);
}



    var instructionsHTML = {
      'str1': ['<p> On each trial, you will see a brief video of a few objects interacting.</p><p>Your task will be to predict whether \
      a certain event will happen after the video ends.</p><p>Before the video starts, you\'ll see one object flash in red and an area in yellow. Remember these objects! You\'ll be asked if the object marked in red will touch the area marked in yellow.\
      </p><div><img src="img/blinkingdemo.gif"></div><p>You will do a few “warmup” trials first, followed by 150 real trials. For the warmup trials, you will find out whether your response was correct or not, but you won\'t on the real trials.']
    };

    // add consent pages
    consentHTML = {
      'str2': ["<u><p id='legal'>Consent to Participate</p></u>",
        "<p id='legal'>By completing this study, you are participating in a \
      study being performed by cognitive scientists in the UC San Diego \
      Department of Psychology. The purpose of this research is to find out\
      how people understand visual information. \
      You must be at least 18 years old to participate. There are neither\
      specific benefits nor anticipated risks associated with participation\
      in this study. Your participation in this study is completely voluntary\
      and you can withdraw at any time by simply exiting the study. You may \
      decline to answer any or all of the following questions. Choosing not \
      to participate or withdrawing will result in no penalty. Your anonymity \
      is assured; the researchers who have requested your participation will \
      not receive any personal information about you, and any information you \
      provide will not be shared in association with any personally identifying \
      information.</p>"
      ].join(' '),
      'str3': ["<u><p id='legal'>Consent to Participate</p></u>",
        "<p> If you have questions about this research, please contact the \
      researchers by sending an email to \
      <b><a href='mailto://cogtoolslab.requester@gmail.com'>cogtoolslab.requester@gmail.com</a></b>. \
      These researchers will do their best to communicate with you in a timely, \
      professional, and courteous manner. If you have questions regarding your \
      rights as a research subject, or if problems arise which you do not feel \
      you can discuss with the researchers, please contact the UC San Diego \
      Institutional Review Board.</p><p>Click 'Next' to continue \
      participating in this study.</p>"
      ].join(' '),
      'str4': '<p> We expect this study to take approximately 10 to 15 minutes to complete, \
      including the time it takes to read these instructions.</p>',
      'str5': "<p>If you encounter a problem or error, send us an email \
      (cogtoolslab.requester@gmail.com) and we will make sure you're compensated \
      for your time! Please pay attention and do your best! Thank you!</p><p> Note: \
        We recommend using Firefox or Chrome. We have not tested this study in other browsers.</p>"
    };

    //combine instructions and consent
    var introMsg = {
      type: 'instructions',
      pages: [
        // consentHTML.str1,
        consentHTML.str2,
        consentHTML.str3,
        instructionsHTML.str1,
        // instructionsHTML.str2,
        // instructionsHTML.str3,
        consentHTML.str4,
        consentHTML.str5,
        // instructionsHTML.str5,
      ],

      show_clickable_nav: true,
      allow_backward: true,
      delay: false,
      delayTime: 2000,
    };


    // exit survey trials
    var exitSurveyAge = {
      type: 'survey-text',
      on_finish: main_on_finish,
      questions: [
        { prompt: "How old are you?", rows: 1, columns: 3, name: "participantAge", placeholder: "Age" },
      ]
    }
    var exitSurveyChoice =  {
      type: 'survey-multi-choice',
      on_finish: main_on_finish,
      preamble: "<strong><u>Survey</u></strong>",
      questions: [{
        prompt: "What is your sex?",
        name: "participantSex",
        horizontal: true,
        options: ["Male", "Female", "Neither/Other/Do Not Wish To Say"],
        required: true
      },
      // {
      //   prompt: "How old are you?",
      //   name: "participantAge",
      //   horizontal: false,
      //   options: [
      //     "Under 12 years old",
      //     "12-17 years old",
      //     "18-24 years old",
      //     "25-34 years old",
      //     "35-44 years old",
      //     "45-54 years old",
      //     "55-64 years old",
      //     "65-74 years old",
      //     "75 years or older",
      //     ],
      //   required: true
      // },
      {
        prompt: "What is the highest level of education you have completed?",
        name: "participantEducation",
        horizontal: false,
        options: [
          "High school",
          "Some high school",
          "Bachelor’s degree",
          "Master’s degree",
          "Ph.D. or higher",
          "Associates degree",
          "Trade school",
          "Prefer not to say",
          "Other",
          ],
        required: true
      },
      {
        prompt: "Did you encounter any technical difficulties while completing this study? \
            This could include: images were glitchy (e.g., did not load), ability to click \
            was glitchy, or sections of the study did \
            not load properly.",
        name: "technicalDifficultiesBinary",
        horizontal: true,
        options: ["Yes", "No"],
        required: true
      }
      ]
    };

    var surveyTextInfo = _.omit(_.extend({}, new Experiment), ['type', 'dev_mode']);
    var exitSurveyText = _.extend({}, surveyTextInfo, {
      type: 'survey-text',      
      questions: [
        { prompt: "What strategies did you use to predict what will happen?", rows: 5, columns: 40 },
        // { prompt: "What criteria mattered most when evaluating " + experimentInstance.condition + "?", rows: 5, columns: 40 },
        // { prompt: "What criteria did not matter when evaluating " + experimentInstance.condition + "?", rows: 5, columns: 40 },
        // { prompt: "Any final thoughts?", rows: 5, columns: 40 }
      ],
      on_finish: main_on_finish
    });

    // add goodbye page
    var goodbye = {
      type: 'instructions',
      pages: [
        'Congrats! You are all done. Thanks for participating in our game. \  Click \'Next\' to submit this study.',
      ],
      on_start: (trial) => { //write the score to HTML
        trial.pages = [
          'Congrats! You are all done. Thanks for participating in our game. \ You\'ve gotten '+_.round((correct/total)*100,0)+'% correct🎉! Click \'Next\' to submit this study.',
        ];
      },
      show_clickable_nav: true,
      allow_backward: false,
      delay: false,
      on_finish: function() {
        // $(".confetti").remove();
        document.body.innerHTML = '<p> Please wait. You will be redirected back to Prolific in a few moments.</p>'
                setTimeout(function () { location.href = "https://app.prolific.co/submissions/complete?cc=50AEDCF9" }, 500)
        // sendData();
      }
      //change the link below to your prolific-provided URL
      // window.open("https://app.prolific.co/submissions/complete?cc=7A827F20","_self");
    };

    // mental rotation task
    var mentalRotationChoice = {
      type: 'image-button-response',
      image_url: 'img/shepard_metzler_rotation_task_1.png', //taken from http://dx.doi.org/10.1109/CTS.2009.5067476
      choices: ['A', 'B', 'C'],
      upper_bound: '',
      lower_bound: '',
      prompt: "Which of the three objects on the right is a rotated version of the object on the left?",
      on_finish: main_on_finish
    };

    // add all experiment elements to trials array
    if (includeFamiliarizationTrials) trials = _.concat(familiarization_trials, trials);
    if (includeIntro) trials.unshift(introMsg);
    if (includeSurvey) trials.push(exitSurveyText);
    if (includeSurvey) trials.push(exitSurveyChoice);
    if (includeSurvey) trials.push(exitSurveyAge);
    // if (includeMentalRotation) trials.push(mentalRotationChoice);
    if (includeGoodbye) trials.push(goodbye);


    jsPsych.init({
      timeline: trials,
      default_iti: 1000,
      show_progress_bar: true
    });

  }); // close onConnected
} // close setup game
