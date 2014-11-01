'use strict';
$(document).ready(function() {
    var ws;
    var fogBtn = $('#fogBtn');
    
    function touchstartHandler() {
      sendMessage('FOG:START');
    }
    function touchendHandler() {
      sendMessage('FOG:END');
    }

    function openWS() {
      ws = new WebSocket('ws://'+window.location.host+'/ws');
      ws.onmessage = function(e) {
        var filename = e.data
        filename = filename.substring(filename.lastIndexOf('/')+1)
        // $('#status').text($('#nextfile').text())
        // $('#nextfile').text(filename)
      };
      ws.onclose = function() {
        openWS();
      };
    }

    function sendMessage(message) {
      if(message) {
        ws.send(message);
      }
    }

    var status = $('#status');
    if('WebSocket' in window) {
        status.text('');
        openWS();
      }
    else {
        status.text('WebSockets are NOT supported by your browser!');
    }
    
    fogBtn.bind('touchstart', touchstartHandler);
    fogBtn.bind('touchend', touchendHandler);

    //disable longpress
    // $('.no-touch-callout').each(function(index, el) {
    //  $(el).bind('touchstart', function(e) {
    //      e.preventDefault();
    //  });
    // });
});