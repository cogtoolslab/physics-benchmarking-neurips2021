/**
 * jspsych-video-overlay-button-response
 * Josh de Leeuw
 *
 * plugin for playing a video file and getting a button response.
 *
 * ADAPTED to hide the video after stopping it—DO NOT simply overwrite.
 * 
 * documentation: docs.jspsych.org
 *
 **/

 jsPsych.plugins["video-overlay-button-response"] = (function() {

  var plugin = {};

  jsPsych.pluginAPI.registerPreload('video-overlay-button-response', 'stimulus', 'video');
  jsPsych.pluginAPI.registerPreload('video-overlay-button-response', 'overlay', 'image');

  plugin.info = {
    name: 'video-overlay-button-response',
    description: '',
    parameters: {
      stimulus: {
        type: jsPsych.plugins.parameterType.VIDEO,
        pretty_name: 'Video',
        default: undefined,
        description: 'The video file to play.'
      },
      overlay: {
        type: jsPsych.plugins.parameterType.IMAGE,
        pretty_name: 'Overlay',
        default: null,
        description: 'The overlay to place over the video before it starts.'
      },
      choices: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Choices',
        default: undefined,
        array: true,
        description: 'The labels for the buttons.'
      },
      button_html: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Button HTML',
        default: '<button class="jspsych-btn">%choice%</button>',
        array: true,
        description: 'The html of the button. Can create own style.'
      },
      prompt: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Prompt',
        default: null,
        description: 'Any content here will be displayed below the buttons.'
      },
      width: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Width',
        default: '',
        description: 'The width of the video in pixels.'
      },
      height: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Height',
        default: '',
        description: 'The height of the video display in pixels.'
      },
      autoplay: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Autoplay',
        default: false,
        description: 'If true, the video will begin playing as soon as it has loaded.'
      },
      controls: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Controls',
        default: false,
        description: 'If true, the subject will be able to pause the video or move the playback to any point in the video.'
      },
      start: {
        type: jsPsych.plugins.parameterType.FLOAT,
        pretty_name: 'Start',
        default: 0,
        description: 'Time to start the clip.'
      },
      stop: {
        type: jsPsych.plugins.parameterType.FLOAT,
        pretty_name: 'Stop',
        default: null,
        description: 'Time to stop the clip.'
      },
      overlay_time: {
        type: jsPsych.plugins.parameterType.FLOAT,
        pretty_name: 'OverlayTime',
        default: 3.,
        description: 'How long to show the first frame and the overlay.'
      },
      blink_time: {
        type: jsPsych.plugins.parameterType.FLOAT,
        pretty_name: 'OverlayTime',
        default: 250,
        description: 'Length of blinks in milliseconds.'
      },
      rate: {
        type: jsPsych.plugins.parameterType.FLOAT,
        pretty_name: 'Rate',
        default: 1,
        description: 'The playback rate of the video. 1 is normal, <1 is slower, >1 is faster.'
      },
      trial_ends_after_video: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'End trial after video finishes',
        default: false,
        description: 'If true, the trial will end immediately after the video finishes playing.'
      },
      trial_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Trial duration',
        default: null,
        description: 'How long to show trial before it ends.'
      },
      margin_vertical: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Margin vertical',
        default: '0px',
        description: 'The vertical margin of the button.'
      },
      margin_horizontal: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Margin horizontal',
        default: '8px',
        description: 'The horizontal margin of the button.'
      },
      response_ends_trial: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Response ends trial',
        default: true,
        description: 'If true, the trial will end when subject makes a response.'
      },
      response_allowed_while_playing: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Response allowed while playing',
        default: false,
        description: 'If true, then responses are allowed while the video is playing. '+
          'If false, then the video must finish playing before a response is accepted.'
      }
    }
  }

  plugin.trial = function(display_element, trial) {

    // setup stimulus
    var video_html = '<div>'
    video_html += '<video id="jspsych-video-overlay-button-response-stimulus"';

    if(trial.width) {
      video_html += ' width="'+trial.width+'"';
    }
    if(trial.height) {
      video_html += ' height="'+trial.height+'"';
    }
    // if(trial.autoplay & (trial.start == null)){
    //   // if autoplay is true and the start time is specified, then the video will start automatically
    //   // via the play() method, rather than the autoplay attribute, to prevent showing the first frame
    //   video_html += " autoplay ";
    // }
    if(trial.controls){
      video_html +=" controls ";
    }
    // if (trial.start !== null) {
    //   // hide video element when page loads if the start time is specified, 
    //   // to prevent the video element from showing the first frame
    //   video_html += ' style="visibility: hidden;"'; 
    // }
    video_html +=">";
    
    //preloading blobs doesn't work for safari
    //HACK turn off preloading for Safari
    var isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent); // https://stackoverflow.com/questions/7944460/detect-safari-browser#23522755
    
    var video_preload_blob = jsPsych.pluginAPI.getVideoBuffer(trial.stimulus[0]);
    if(isSafari){
      video_preload_blob = false;
      console.log("Turning off preloading for Safari. Additional delay possible.");
    }
    if(!video_preload_blob) {
      for(var i=0; i<trial.stimulus.length; i++){
        var file_name = trial.stimulus[i];
        if (DEBUG_MODE){console.log("Loading stim"+file_name);}
        if(file_name.indexOf('?') > -1){
          file_name = file_name.substring(0, file_name.indexOf('?'));
        }
        var type = file_name.substr(file_name.lastIndexOf('.') + 1);
        type = type.toLowerCase();
        if (type == "mov") {
          console.warn('Warning: video-overlay-button-response plugin does not reliably support .mov files.')
        }
        video_html+='<source src="' + file_name + '" type="video/'+type+'">';   
      }
    }
    video_html += "</video>";
    
    //save the html using only the video
    video_html_1 = video_html;
    //add the image
    if (trial.overlay != null){
      overlay_html = '<image id="jspsych-video-overlay-button-response-overlay"';
      if(trial.width) {
        overlay_html += ' width="'+trial.width+'"';
      }
      if(trial.height) {
        overlay_html += ' height="'+trial.height+'"';
      }   
      overlay_html += 'src="' + trial.overlay + '"';
      overlay_html += 'style = "position: absolute;  margin-left: -' + trial.width + 'px;"';
      overlay_html += '/image>';
      //done adding the image
      video_html += overlay_html;
    }
    video_html_2 = "</div>";

    //display buttons
    var buttons = [];
    if (Array.isArray(trial.button_html)) {
      if (trial.button_html.length == trial.choices.length) {
        buttons = trial.button_html;
      } else {
        console.error('Error in video-overlay-button-response plugin. The length of the button_html array does not equal the length of the choices array');
      }
    } else {
      for (var i = 0; i < trial.choices.length; i++) {
        buttons.push(trial.button_html);
      }
    }
    video_html_2 += '<div id="jspsych-video-overlay-button-response-btngroup">';
    for (var i = 0; i < trial.choices.length; i++) {
      var str = buttons[i].replace(/%choice%/g, trial.choices[i]);
      video_html_2 += '<div class="jspsych-video-overlay-button-response-button" style="cursor: pointer; display: inline-block; margin:'+trial.margin_vertical+' '+trial.margin_horizontal+'" id="jspsych-video-overlay-button-response-button-' + i +'" data-choice="'+i+'">'+str+'</div>';
    }
    video_html_2 += '</div>';

    // add prompt if there is one
    if (trial.prompt !== null) {
      video_html_2 += trial.prompt;
    }
    
    display_element.innerHTML = video_html_1 + overlay_html + video_html_2;
    
    var video_element = display_element.querySelector('#jspsych-video-overlay-button-response-stimulus');
    var overlay_element = display_element.querySelector('#jspsych-video-overlay-button-response-overlay');    
    
    if(video_preload_blob){video_element.src = video_preload_blob;}
    disable_buttons();
    video_element.onended = function(){
      if(trial.trial_ends_after_video){
        end_trial();
      } else if (!trial.response_allowed_while_playing) {
        enable_buttons();
      }
    }
  
    video_element.playbackRate = trial.rate;
  
    if(trial.stop !== null){
      video_element.addEventListener('timeupdate', function(e){
        var currenttime = video_element.currentTime;
        if(currenttime >= trial.stop){
          video_element.pause();
          video_element.style.visibility = "hidden"; //hide the video after stop
          enable_buttons(); //enable response after video stopped
        }
      })
    }
    var start_time = performance.now();

    //wait and then start the trial
    if (trial.overlay != null){
    jsPsych.pluginAPI.setTimeout(hide_overlay_and_start,trial.overlay_time*1000);
    } else{
    hide_overlay_and_start();
    }

    //set up blinks
    if (trial.overlay != null){
      hidden = true;
      _.range(0,trial.overlay_time*1000,trial.blink_time).forEach(
        t => {
          if(hidden){
            jsPsych.pluginAPI.setTimeout(() => {overlay_element.hidden = true;}, t);}
            else{
              jsPsych.pluginAPI.setTimeout(() => {overlay_element.hidden = false;}, t);}
          hidden = !hidden;
        }
      )
    }
      
    function hide_overlay_and_start() {
      overlay_element.hidden = true;
      video_element.play();
    }
    

    if(trial.response_allowed_while_playing){
      enable_buttons();
    } else {
      disable_buttons();
    }

    // store response
    var response = {
      rt: null,
      button: null
    };

    // function to end trial when it is time
    function end_trial() {

      // kill any remaining setTimeout handlers
      jsPsych.pluginAPI.clearAllTimeouts();

      // stop the video file if it is playing
      // remove any remaining end event handlers
      display_element.querySelector('#jspsych-video-overlay-button-response-stimulus').pause();
      display_element.querySelector('#jspsych-video-overlay-button-response-stimulus').onended = function() {};

      // gather the data to store for the trial
      var trial_data = {
        rt: response.rt,
        stimulus: trial.stimulus,
        response: trial.choices[response.button] //return the button label instead of index
      };

      // clear the display
      display_element.innerHTML = '';

      // move on to the next trial
      jsPsych.finishTrial(trial_data);
    }

    // function to handle responses by the subject
    function after_response(choice) {

      // measure rt
      var end_time = performance.now();
      var rt = end_time - start_time;
      response.button = parseInt(choice);
      response.rt = rt;

      // after a valid response, the stimulus will have the CSS class 'responded'
      // which can be used to provide visual feedback that a response was recorded
      video_element.className += ' responded';

      // disable all the buttons after a response
      disable_buttons();

      if (trial.response_ends_trial) {
        end_trial();
      }
    }

    function button_response(e){
      var choice = e.currentTarget.getAttribute('data-choice'); // don't use dataset for jsdom compatibility
      after_response(choice);
    }

    function disable_buttons() {
      var btns = document.querySelectorAll('.jspsych-video-overlay-button-response-button');
      for (var i=0; i<btns.length; i++) {
        var btn_el = btns[i].querySelector('button');
        if(btn_el){
          btn_el.disabled = true;
        }
        btns[i].removeEventListener('click', button_response);
      }
    }

    function enable_buttons() {
      var btns = document.querySelectorAll('.jspsych-video-overlay-button-response-button');
      for (var i=0; i<btns.length; i++) {
        var btn_el = btns[i].querySelector('button');
        if(btn_el){
          btn_el.disabled = false;
        }
        btns[i].addEventListener('click', button_response);
      }
    }

    // end trial if time limit is set
    if (trial.trial_duration !== null) {
      jsPsych.pluginAPI.setTimeout(function() {
        end_trial();
      }, trial.trial_duration);
    }
  };

  return plugin;
})();
