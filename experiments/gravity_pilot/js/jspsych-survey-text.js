/**
 * jspsych-survey-text
 * a jspsych plugin for free response survey questions
 *
 * Josh de Leeuw
 *
 * documentation: docs.jspsych.org
 * minor edits by Holly Huey, so that text box and inside text is aligned left
 */

/**
 * jspsych-survey-text
 * a jspsych plugin for free response survey questions
 *
 * Josh de Leeuw
 *
 * documentation: docs.jspsych.org
 *
 */


jsPsych.plugins['survey-text'] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'survey-text',
    description: '',
    parameters: {
      questions: {
        type: jsPsych.plugins.parameterType.COMPLEX,
        array: true,
        pretty_name: 'Questions',
        default: undefined,
        nested: {
          prompt: {
            type: jsPsych.plugins.parameterType.STRING,
            pretty_name: 'Prompt',
            default: undefined,
            description: 'Prompt for the subject to response'
          },
          placeholder: {
            type: jsPsych.plugins.parameterType.STRING,
            pretty_name: 'Value',
            default: "",
            description: 'Placeholder text in the textfield.'
          },
          rows: {
            type: jsPsych.plugins.parameterType.INT,
            pretty_name: 'Rows',
            default: 1,
            description: 'The number of rows for the response text box.'
          },
          columns: {
            type: jsPsych.plugins.parameterType.INT,
            pretty_name: 'Columns',
            default: 40,
            description: 'The number of columns for the response text box.'
          },
          required: {
            type: jsPsych.plugins.parameterType.BOOL,
            pretty_name: 'Required',
            default: false,
            description: 'Require a response'
          },
          name: {
            type: jsPsych.plugins.parameterType.STRING,
            pretty_name: 'Question Name',
            default: '',
            description: 'Controls the name of data values associated with this question'
          }
        }
      },
      preamble: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Preamble',
        default: null,
        description: 'HTML formatted string to display at the top of the page above all the questions.'
      },
      button_label: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Button label',
        default:  'Continue',
        description: 'The text that appears on the button to finish the trial.'
      },
      dbname: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'MongoDB dbname',
        default: 'causaldraw',
        description: 'name of database to insert survey data into'
      },
      colname: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'MongoDB collection name',
        default: 'machines',
        description: 'name of collection to insert survey data into'
      },      
      iterationName: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'iteration name',
        default: 'surveyData',
        description: 'informal name of experiment iteration'
      },        
      gameID: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'gameID',
        default: 'surveyData',
        description: 'participant ID'
      }                 
    }
  }

  plugin.trial = function(display_element, trial) {

    for (var i = 0; i < trial.questions.length; i++) {
      if (typeof trial.questions[i].rows == 'undefined') {
        trial.questions[i].rows = 1;
      }
    }
    for (var i = 0; i < trial.questions.length; i++) {
      if (typeof trial.questions[i].columns == 'undefined') {
        trial.questions[i].columns = 40;
      }
    }
    for (var i = 0; i < trial.questions.length; i++) {
      if (typeof trial.questions[i].value == 'undefined') {
        trial.questions[i].value = "";
      }
    }

    var html = '';
    // show preamble text
    if(trial.preamble !== null){
      html += '<div id="jspsych-survey-text-preamble" class="jspsych-survey-text-preamble">'+trial.preamble+'</div>';
    }
    // start form
    html += '<form id="jspsych-survey-text-form">'

    // generate question order
    var question_order = [];
    for(var i=0; i<trial.questions.length; i++){
      question_order.push(i);
    }
    if(trial.randomize_question_order){
      question_order = jsPsych.randomization.shuffle(question_order);
    }

    // add questions
    for (var i = 0; i < trial.questions.length; i++) {
      var question = trial.questions[question_order[i]];
      var question_index = question_order[i];
      html += '<div id="jspsych-survey-text-'+question_index+'" class="jspsych-survey-text-question" style="margin: 2em 0em;">';
      html += '<p class="jspsych-survey-text">' + question.prompt + '</p>';
      var autofocus = i == 0 ? "autofocus" : "";
      var req = question.required ? "required" : "";
      if(question.rows == 1){
        html += '<input type="text" id="input-'+question_index+'"  name="#jspsych-survey-text-response-' + question_index + '" data-name="'+question.name+'" size="'+question.columns+'" '+autofocus+' '+req+' placeholder="'+question.placeholder+'"></input>';
      } else {
        html += '<textarea id="input-'+question_index+'" name="#jspsych-survey-text-response-' + question_index + '" data-name="'+question.name+'" cols="' + question.columns + '" rows="' + question.rows + '" '+autofocus+' '+req+' placeholder="'+question.placeholder+'"></textarea>';
      }
      html += '</div>';
    }

    // add submit button
    html += '<input type="submit" id="jspsych-survey-text-next" class="jspsych-btn jspsych-survey-text" value="'+trial.button_label+'"></input>';

    html += '</form>'
    display_element.innerHTML = html;

    // backup in case autofocus doesn't work
    display_element.querySelector('#input-'+question_order[0]).focus();

    display_element.querySelector('#jspsych-survey-text-form').addEventListener('submit', function(e) {
      e.preventDefault();
      // measure response time
      var endTime = performance.now();
      var response_time = endTime - startTime;

      // create object to hold responses
      var question_data = {};
      
      for(var index=0; index < trial.questions.length; index++){
        var id = "Q" + index;
        var q_element = document.querySelector('#jspsych-survey-text-'+index).querySelector('textarea, input'); 
        var val = q_element.value;
        var name = q_element.attributes['data-name'].value;
        if(name == ''){
          name = id;
        }        
        var obje = {};
        obje[name] = val;
        Object.assign(question_data, obje);
      }

      // extract worker info
      var turkInfo = jsPsych.turk.turkInfo();

      // save data
      var trial_data = {
        workerId: turkInfo.workerId,
        hitID: turkInfo.hitId,
        aID: turkInfo.assignmentId,
        gameID: trial.gameID,
        dbname: trial.dbname,
        colname: trial.colname,
        iterationName: trial.iterationName,   
        eventType: 'survey',       
        rt: response_time,
        responses: JSON.stringify(question_data)
      };

      display_element.innerHTML = '';

      // next trial
      jsPsych.finishTrial(trial_data);
    });

    var startTime = performance.now();
  };

  return plugin;
})();

// jsPsych.plugins['survey-text'] = (function() {

//     var plugin = {};
  
//     plugin.info = {
//       name: 'survey-text',
//       description: '',
//       parameters: {
//         questions: {
//           type: jsPsych.plugins.parameterType.COMPLEX,
//           array: true,
//           pretty_name: 'Questions',
//           default: undefined,
//           nested: {
//             prompt: {
//               type: jsPsych.plugins.parameterType.STRING,
//               pretty_name: 'Prompt',
//               default: undefined,
//               description: 'Prompt for the subject to response'
//             },
//             placeholder: {
//               type: jsPsych.plugins.parameterType.STRING,
//               pretty_name: 'Value',
//               default: "",
//               description: 'Placeholder text in the textfield.'
//             },
//             rows: {
//               type: jsPsych.plugins.parameterType.INT,
//               pretty_name: 'Rows',
//               default: 1,
//               description: 'The number of rows for the response text box.'
//             },
//             columns: {
//               type: jsPsych.plugins.parameterType.INT,
//               pretty_name: 'Columns',
//               default: 40,
//               description: 'The number of columns for the response text box.'
//             },
//             required: {
//               type: jsPsych.plugins.parameterType.BOOL,
//               pretty_name: 'Required',
//               default: false,
//               description: 'Require a response'
//             },
//             name: {
//               type: jsPsych.plugins.parameterType.STRING,
//               pretty_name: 'Question Name',
//               default: '',
//               description: 'Controls the name of data values associated with this question'
//             }
//           }
//         },
//         preamble: {
//           type: jsPsych.plugins.parameterType.STRING,
//           pretty_name: 'Preamble',
//           default: null,
//           description: 'HTML formatted string to display at the top of the page above all the questions.'
//         },
//         button_label: {
//           type: jsPsych.plugins.parameterType.STRING,
//           pretty_name: 'Button label',
//           default:  'Continue',
//           description: 'The text that appears on the button to finish the trial.'
//         },
//         dbname: {
//           type: jsPsych.plugins.parameterType.STRING,
//           pretty_name: 'MongoDB dbname',
//           default: 'causaldraw',
//           description: 'name of database to insert survey data into'
//         },
//         colname: {
//           type: jsPsych.plugins.parameterType.STRING,
//           pretty_name: 'MongoDB collection name',
//           default: 'machines',
//           description: 'name of collection to insert survey data into'
//         },      
//         iterationName: {
//           type: jsPsych.plugins.parameterType.STRING,
//           pretty_name: 'iteration name',
//           default: 'surveyData',
//           description: 'informal name of experiment iteration'
//         }         
//       }
//     }
  
//     plugin.trial = function(display_element, trial) {
  
//       for (var i = 0; i < trial.questions.length; i++) {
//         if (typeof trial.questions[i].rows == 'undefined') {
//           trial.questions[i].rows = 1;
//         }
//       }
//       for (var i = 0; i < trial.questions.length; i++) {
//         if (typeof trial.questions[i].columns == 'undefined') {
//           trial.questions[i].columns = 40;
//         }
//       }
//       for (var i = 0; i < trial.questions.length; i++) {
//         if (typeof trial.questions[i].value == 'undefined') {
//           trial.questions[i].value = "";
//         }
//       }
  
//       var html = '';
//       // show preamble text
//       if(trial.preamble !== null){
//         html += '<div id="jspsych-survey-text-preamble" class="jspsych-survey-text-preamble">'+trial.preamble+'</div>';
//       }
//       // start form
//       html += '<form id="jspsych-survey-text-form">'
  
//       // generate question order
//       var question_order = [];
//       for(var i=0; i<trial.questions.length; i++){
//         question_order.push(i);
//       }
//       if(trial.randomize_question_order){
//         question_order = jsPsych.randomization.shuffle(question_order);
//       }
  
//       // add questions
//       for (var i = 0; i < trial.questions.length; i++) {
//         var question = trial.questions[question_order[i]];
//         var question_index = question_order[i];
//         html += '<div id="jspsych-survey-text-'+question_index+'" class="jspsych-survey-text-question" style="margin: 2em 0em; text-align: left">'; 
//         html += '<p class="jspsych-survey-text" style="text-align: left;">' + question.prompt + '</p>';
//         var autofocus = i == 0 ? "autofocus" : "";
//         var req = question.required ? "required" : "";
//         if(question.rows == 1){
//           html += '<input type="text" style="margin: 0em 0em; text-align: left" id="input-'+question_index+'" name="#jspsych-survey-text-response-' + question_index + '" data-name="'+question.name+'" size="'+question.columns+'" '+autofocus+' '+req+' placeholder="'+question.placeholder+'"></input>'; 
//         } else {
//           html += '<textarea style="margin: 0em 0em; text-align: left" id="input-'+question_index+'" name="#jspsych-survey-text-response-' + question_index + '" data-name="'+question.name+'" cols="' + question.columns + '" rows="' + question.rows + '" '+autofocus+' '+req+' placeholder="'+question.placeholder+'"></textarea>'; 
//         }
//         html += '</div>';
//       }
  
//       // add submit button
//       html += '<input type="submit" id="jspsych-survey-text-next" class="jspsych-btn jspsych-survey-text" value="'+trial.button_label+'"></input>';
  
//       html += '</form>'
//       display_element.innerHTML = html;
  
//       // backup in case autofocus doesn't work
//       display_element.querySelector('#input-'+question_order[0]).focus();
  
//       display_element.querySelector('#jspsych-survey-text-form').addEventListener('submit', function(e) {
//         e.preventDefault();
//         // measure response time
//         var endTime = performance.now();
//         var response_time = endTime - startTime;
  
//         // create object to hold responses
//         var question_data = {};
        
//         for(var index=0; index < trial.questions.length; index++){
//           var id = "Q" + index;
//           var q_element = document.querySelector('#jspsych-survey-text-'+index).querySelector('textarea, input'); 
//           var val = q_element.value;
//           var name = q_element.attributes['data-name'].value;
//           if(name == ''){
//             name = id;
//           }        
//           var obje = {};
//           obje[name] = val;
//           Object.assign(question_data, obje);
//         }

//         // extract worker info
//         var turkInfo = jsPsych.turk.turkInfo();

//         // save data
//         var trial_data = {
//           workerId: turkInfo.workerId,
//           hitID: turkInfo.hitId,
//           aID: turkInfo.assignmentId,
//           dbname: trial.dbname,
//           colname: trial.colname,
//           iterationName: trial.iterationName,   
//           eventType: 'survey',       
//           rt: response_time,
//           responses: JSON.stringify(question_data)
//         };
  
//         display_element.innerHTML = '';
  
//         // next trial
//         jsPsych.finishTrial(trial_data);
//       });
  
//       var startTime = performance.now();
//     };
  
//     return plugin;
//   })();