/* jspsych-instructions.js
 * Josh de Leeuw, Judy Fan
 *
 * This plugin displays text (including HTML formatted strings) during the experiment.
 * Use it to show instructions, provide performance feedback, etc...
 *
 * Page numbers can be displayed to help with navigation by setting show_page_number
 * to true.
 *
 * documentation: docs.jspsych.org
 *
 * Hijacked so that the nav buttons are displayed 2s after presentation of a new page
 */

jsPsych.plugins.instructions = (function() {

  var plugin = {};

  plugin.info = {
    name: 'instructions',
    description: '',
    parameters: {
      pages: {
        type: jsPsych.plugins.parameterType.HTML_STRING,
        pretty_name: 'Pages',
        default: undefined,
        array: true,
        description: 'Each element of the array is the content for a single page.'
      },
      key_forward: {
        type: jsPsych.plugins.parameterType.KEYCODE,
        pretty_name: 'Key forward',
        default: 'rightarrow', 
        description: 'The key the subject can press in order to advance to the next page.'
      },
      key_backward: {
        type: jsPsych.plugins.parameterType.KEYCODE,
        pretty_name: 'Key backward',
        default: 'leftarrow', 
        description: 'The key that the subject can press to return to the previous page.'
      },
      allow_backward: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Allow backward',
        default: true, 
        description: 'If true, the subject can return to the previous page of the instructions.' //also need uncomment display_element.querySelector('#jspsych-instructions-back')
      },
      allow_keys: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Allow keys',
        default: false,
        description: 'If true, the subject can use keyboard keys to navigate the pages.'
      },
      show_clickable_nav: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Show clickable nav',
        default: false, 
        description: 'If true, then a "Previous" and "Next" button will be displayed beneath the instructions.'
      },
      show_page_number: {
          type: jsPsych.plugins.parameterType.BOOL,
          pretty_name: 'Show page number',
          default: false,
          description: 'If true, and clickable navigation is enabled, then Page x/y will be shown between the nav buttons.'
      },
      button_label_previous: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Button label previous',
        default: 'Previous',
        description: 'The text that appears on the button to go backwards.'
      },
      button_label_next: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Button label next',
        default: 'Next',
        description: 'The text that appears on the button to go forwards.'
      },
      delay: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Presentation of "Previous" and "Next" buttons',
        default: false,
        description: 'If true, delay the presentation of nav buttons'
      }, 
      delayTime: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'Delay of "Previous" and "Next" buttons',
        default: null,
        description: 'If delay is true, delay the presentation of nav buttons by 2000ms'
      }
    }
  }

  plugin.trial = function(display_element, trial) {

    var current_page = 0;
    var view_history = [];
    var start_time = (new Date()).getTime();
    var last_page_update_time = start_time;
    var delayNav = trial.delay ? trial.delayTime : 0;

    function btnListener(evt){
    	evt.target.removeEventListener('click', btnListener);
    	if(this.id === "jspsych-instructions-back"){
    		back();
    	}
    	else if(this.id === 'jspsych-instructions-next'){
    		next();
    	}
    }

    function show_current_page() {
      var html = trial.pages[current_page];
      var pagenum_display = "";
      if(trial.show_page_number) {
          pagenum_display = "<span style='margin: 0 1em;' class='"+
          "jspsych-instructions-pagenum'>Page "+(current_page+1)+"/"+trial.pages.length+"</span>";
      }

      display_element.innerHTML = html;

      if (trial.show_clickable_nav) {

        var nav_html = "<div class='jspsych-instructions-nav' style='padding: 10px 0px;'>";

        if (trial.allow_backward) {
          var allowed = (current_page > 0 )? '' : "disabled='disabled'";
          nav_html += "<button id='jspsych-instructions-back' class='jspsych-btn' style='margin-right: 5px;' "+allowed+">&lt; "+trial.button_label_previous+"</button>";
        }
        
        if (trial.pages.length > 1 && trial.show_page_number) {
            nav_html += pagenum_display;
        }        

        nav_html += "<button id='jspsych-instructions-next' class='jspsych-btn'"+
            "style='margin-left: 5px;'>"+trial.button_label_next+
            " </button></div>";

        // // Place cue video inside the cue video container (which has fixed location)
        // html += '<div id="cue_container" style="display:none">';
        // var cue_html_replaced = trial.dev_mode ? trial.cue_html.replace('stim_url', devModeCue): trial.cue_html.replace('stim_url', trial.stim_url);      
        // // console.log('trial inside show_cue',trial.file_id);
        // html += cue_html_replaced;
        // html += '</div>';

        display_element.innerHTML += nav_html;

        
        // set button text and border to white until it is time to click
        display_element.querySelector('#jspsych-instructions-next').style.color = '#fff';
        display_element.querySelector('#jspsych-instructions-next').style.borderColor = '#fff';
        // display_element.querySelector('#jspsych-instructions-back').style.color = '#fff'; //uncommment and set allow_backwards = true
        // display_element.querySelector('#jspsych-instructions-back').style.borderColor = '#fff'; //uncommment and set allow_backwards = true

        // delay showing nav buttons for delayNav duration
        setTimeout(function(){activateNav();},delayNav);

      } else {
        if (trial.show_page_number && trial.pages.length > 1) {
          // page numbers for non-mouse navigation
          var page_num = "<div class='jspsych-instructions-pagenum'>"+pagenum_display+"</div>";
        } 
        display_element.innerHTML += page_num;
      }
           
    }

    function activateNav() {            

      // now make the colors of the text the appropriate ones
      display_element.querySelector('#jspsych-instructions-next').style.color = '#333';
      display_element.querySelector('#jspsych-instructions-next').style.borderColor = '#ccc';
      // display_element.querySelector('#jspsych-instructions-back').style.color = '#333'; //uncommment and set allow_backwards = true
      // display_element.querySelector('#jspsych-instructions-back').style.borderColor = '#ccc'; //uncommment and set allow_backwards = true

      if (current_page != 0 && trial.allow_backward) {
        display_element.querySelector('#jspsych-instructions-back').addEventListener('click', btnListener);
      }

      display_element.querySelector('#jspsych-instructions-next').addEventListener('click', btnListener);      
    }


    function next() {

      add_current_page_to_view_history()

      current_page++;

      // if done, finish up...
      if (current_page >= trial.pages.length) {
        endTrial();
      } else {
        show_current_page();
      }

    }

    function back() {

      add_current_page_to_view_history()

      current_page--;

      show_current_page();
    }

    function add_current_page_to_view_history() {

      var current_time = (new Date()).getTime();
      var page_view_time = current_time - last_page_update_time;

      view_history.push({
        page_index: current_page,
        viewing_time: page_view_time
      });

      last_page_update_time = current_time;
    }

    function endTrial() {

      if (trial.allow_keys) {
        jsPsych.pluginAPI.cancelKeyboardResponse(keyboard_listener);
      }

      display_element.innerHTML = '';

      var trial_data = {
        "view_history": JSON.stringify(view_history),
        "rt": (new Date()).getTime() - start_time
      };

      jsPsych.finishTrial(trial_data);
    }

    var after_response = function(info) {

      // have to reinitialize this instead of letting it persist to prevent accidental skips of pages by holding down keys too long
      keyboard_listener = jsPsych.pluginAPI.getKeyboardResponse({
        callback_function: after_response,
        valid_responses: [trial.key_forward, trial.key_backward],
        rt_method: 'date',
        persist: false,
        allow_held_key: false
      });
      // check if key is forwards or backwards and update page
      if (jsPsych.pluginAPI.compareKeys(info.key, trial.key_backward)) {
        if (current_page !== 0 && trial.allow_backward) {
          back();
        }
      }

      if (jsPsych.pluginAPI.compareKeys(info.key, trial.key_forward)) {
        next();
      }

    };

    show_current_page();

    if (trial.allow_keys) {
      var keyboard_listener = jsPsych.pluginAPI.getKeyboardResponse({
        callback_function: after_response,
        valid_responses: [trial.key_forward, trial.key_backward],
        rt_method: 'date',
        persist: false
      });
    }
  };

  return plugin;
})();
