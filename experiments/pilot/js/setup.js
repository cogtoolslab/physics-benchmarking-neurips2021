function sendData(data) {
  console.log('sending data to mturk');
  jsPsych.turk.submitToTurk({
    'score': 0 //this is a dummy placeholder
  });
}

// Define trial object with boilerplate
function Experiment() {
  //cogsci 2020 data (run_0)
  this.type = 'image-button-response',
  // this.dbname = 'curiotower';
  // this.colname = 'tdw-height3Jitter3';
  // this.iterationName = 'run_0';

  this.dbname = 'curiotower';
  this.colname = 'curiodrop';
  this.iterationName = 'run_1';
  // this.numTrials = 6; // TODO: dont hard code this, judy! infer it from the data
  this.condition = 'interesting' //_.sample([0, 1]) == 1 ? 'interesting' : 'stable';
  this.prompt = this.condition == 'interesting' ? 'How interesting is this?' : 'How stable is this?';
};

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
    const includeGoodbye = true;

    var gameid = d.gameid;
    var meta = _.shuffle(d.meta);
    console.log('meta', meta);    
      
    var main_on_start = function (trial) {
      console.log('start of trial');
    };

    // at end of each trial save data locally and send data to server
    var main_on_finish = function (data) {
      socket.emit('currentData', data);
      console.log('emitting data');
    }

    // Now construct trials list    
    var experimentInstance = new Experiment;
    
    // loop over value in meta, then append to each the experiment instance info and the prolific, and trial num
    var trials = _.map(meta, function(n,i) {
      return _.extend({}, experimentInstance, n, {
        trialNum: i,
        on_finish: main_on_finish,
        prolificID:  prolificID,
        studyID: studyID, 
        sessionID: sessionID,
        gameID: gameid
      });
    });


    // var trials = _.map(_.range(experimentInstance.numTrials), function (n, i) {
    //   return _.extend({}, experimentInstance, {
    //     trialNum: i,
    //     on_finish: main_on_finish,
    //     on_start: main_on_start,
    //     image_url: 'URL_PLACEHOLDER',
    //     towerID: 'TOWERID_PLACEHOLDER',
    //   });
    // });

    // var trials = _.flatten(_.map(session.trials, function(trialData, i) {
    //   var trial = _.extend({}, additionalInfo, trialData, {trialNum: i});
    //   return trial;
    // }));
    console.log('trials', trials);




    var instructionsHTML = {
      'str1': ['<p> On each trial, you will see an image of a block structure. Your goal is to rate how '+ experimentInstance.condition + ' it is. \
      The rating scale ranges from 1 (not ' + experimentInstance.condition + ' at all) to 5 (extremely ' + experimentInstance.condition + '). </p> <p>Here are \
      some example towers that should be given a score of 1 and some towers that should be given a score of 5.</p>',
      '<div class="example_images">', 
        '<div class="example_image" style="float:left;">', 
          '<p style="text-align:center;">Example tower with ' + experimentInstance.condition + ' score of 1: </p>',
          '<div class="eg_div"><img class="eg_img" src="assets/example-not-' + experimentInstance.condition + '.jpg" width="200" height="200"></div>',
        '</div>',
        '<div class="example_image" style="float:right;">',
          '<p style="text-align:center;">Example tower with ' + experimentInstance.condition + ' score of 5: </p>',
          '<div class="eg_div"><img class="eg_img" src="assets/example-' + experimentInstance.condition + '.jpg" width="200" height="200"></div>',
        '</div>',
      '</div>'].join(' '),
      // 'str3': ['<p> If you notice any of the following, this should reduce the score you assign to that tracing:</p>',
      //     '<ul><li>Adding extra objects to the tracing (e.g. scribbles, heart, flower, smiling faces, text)<img class="notice_img" src="img/extra.png"></li>',
      //     '<li>Painting or "filling in" the reference shape, rather than tracing its outline<img class="notice_img" src="img/paint.png"></li></ul>',].join(' '),
      'str2': '<p>After a brief two-second delay, \
      the buttons will become active (dark gray) so you can submit your rating. Please take your time to provide as accurate of a rating as you can.</p> </p>',
      'str3': "<p> When you finish, please click the submit button to finish the task. If a popup appears asking you if you are sure you want to leave the page, \
      you must click YES to confirm that you want to leave the page. This will cause the study to submit. Let's begin!"
    };

    // add consent pages
    consentHTML = {
      'str1': '<p style="text-align:center;"> <b> We are scientists interested in understanding how computers can learn like children through play. </b></p> \
      <p style="text-align:center;">In a previous study, we gave children a set of plastic shapes which they could arrange in any way they liked. \
      In this study, you will be viewing some of the arrangements of computer generated towers and making judgments about them. \
      Your task is to rate each tower on a 5-point scale. </p>',
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
      'str4': '<p> We expect this study to take approximately 15-20 minutes to complete, \
      including the time it takes to read instructions.</p>',
      'str5': "<p>If you encounter a problem or error, send us an email \
      (cogtoolslab.requester@gmail.com) and we will make sure you're compensated \
      for your time! Please pay attention and do your best! Thank you!</p><p> Note: \
        We recommend using Chrome. We have not tested this study in other browsers.</p>"

    };

    //combine instructions and consent
    var introMsg = {
      type: 'instructions',
      pages: [
        consentHTML.str1,
        consentHTML.str2,
        consentHTML.str3,
        instructionsHTML.str1,
        instructionsHTML.str2,
        instructionsHTML.str3,
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
    var surveyChoiceInfo = _.omit(_.extend({}, new Experiment), ['type', 'dev_mode']);
    var exitSurveyChoice = _.extend({}, surveyChoiceInfo, {
      type: 'survey-multi-choice',
      preamble: "<strong><u>Survey</u></strong>",
      questions: [{
        prompt: "What is your sex?",
        name: "participantSex",
        horizontal: true,
        options: ["Male", "Female", "Neither/Other/Do Not Wish To Say"],
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
      ],
      on_finish: main_on_finish
    });


    // var exitSurveyChoice = {
    //   type: 'survey-multi-choice',
    //   preamble: "<strong><u>Survey</u></strong>",
    //   questions: [{
    //     prompt: "What is your sex?",
    //     name: "participantSex",
    //     horizontal: true,
    //     options: ["Male", "Female", "Neither/Other/Do Not Wish To Say"],
    //     required: true
    //   },
    //   {
    //     prompt: "Did you encounter any technical difficulties while completing this study? \
    //         This could include: images were glitchy (e.g., did not load), ability to click \
    //         was glitchy, or sections of the study did \
    //         not load properly.",
    //     name: "technicalDifficultiesBinary",
    //     horizontal: true,
    //     options: ["Yes", "No"],
    //     required: true
    //   }
    //   ],
    // };
    var surveyTextInfo = _.omit(_.extend({}, new Experiment), ['type', 'dev_mode']);
    var exitSurveyText = _.extend({}, surveyTextInfo, {
      type: 'survey-text',
      questions: [
        { prompt: "Please enter your age:" },
        { prompt: "What strategies did you use to rate the towers?", rows: 5, columns: 40 },
        { prompt: "What criteria mattered most when evaluating " + experimentInstance.condition + "?", rows: 5, columns: 40 },
        { prompt: "What criteria did not matter when evaluating " + experimentInstance.condition + "?", rows: 5, columns: 40 },
        { prompt: "Any final thoughts?", rows: 5, columns: 40 }
      ],
      on_finish: main_on_finish
    });




    // var exitSurveyText = {
    //   type: 'survey-text',
    //   questions: [
    //     { prompt: "Please enter your age:" },
    //     { prompt: "What strategies did you use to rate the towers?", rows: 5, columns: 40 },
    //     { prompt: "What criteria mattered most when evaluating " + experimentInstance.condition + "?", rows: 5, columns: 40 },
    //     { prompt: "What criteria did not matter when evaluating " + experimentInstance.condition + "?", rows: 5, columns: 40 },
    //     { prompt: "Any final thoughts?", rows: 5, columns: 40 }
    //   ]
    // };

    // add goodbye page
    var goodbye = {
      type: 'instructions',
      pages: [
        'Congrats! You are all done. Thanks for participating in our game! \
        Click NEXT to submit this study.',
      ],
      show_clickable_nav: true,
      allow_backward: false,
      delay: false,
      on_finish: function() {
        // $(".confetti").remove();
        document.body.innerHTML = '<p> Please wait. You will be redirected back to Prolific in a few moments.</p>'
                setTimeout(function () { location.href = "https://app.prolific.co/submissions/complete?cc=34BB0C6B" }, 500)
        sendData();
      }
      //change the link below to your prolific-provided URL
      // window.open("https://app.prolific.co/submissions/complete?cc=7A827F20","_self");
    };

    // add all experiment elements to trials array
    if (includeIntro) trials.unshift(introMsg);
    if (includeSurvey) trials.push(exitSurveyChoice);
    if (includeSurvey) trials.push(exitSurveyText);
    if (includeGoodbye) trials.push(goodbye);


    jsPsych.init({
      timeline: trials,
      default_iti: 1000,
      show_progress_bar: true
    });

  }); // close onConnected
} // close setup game
