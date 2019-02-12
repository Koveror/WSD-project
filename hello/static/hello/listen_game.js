//This script is used for listening embedded games and acting accordingly.
"use strict";

//Helper function for getting cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue =   decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

//Helper function for recognising safe methods
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


//Add event listener here
window.addEventListener("message", receiveMessage, false);

//This function receives the messages sent by the game
function receiveMessage(event)
{
    if(event.origin !== "") {
        //FIXME: Only execute messages from trustworthy sources
    }
    var message = JSON.stringify(event.data);
    console.log("Received object: " + message);

    if(event.data.messageType == "SAVE") {
        saveGame(event);
    }
    if(event.data.messageType == "LOAD_REQUEST") {
        loadGame(event);
    }
    if(event.data.messageType == "SCORE") {
        submitScore(event);
    }
}

//Save game state to database
function saveGame(event) {
    //Find the save form in the HTML to get a nicely formatted URL
    var form = $("#save_form");
    var url = form.attr('url');

    $.ajax({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
    type: "POST",
    url: url,
    data: JSON.stringify(event.data),
    dataType: "json"
    }).done(function(save_message) {
    alert(save_message.message);
    });
}

//Load gameState from database and send it to the game
function loadGame(event) {

}

//Save score to the database
function submitScore(event) {
    var form = $("#score_form");
    var url = form.attr('url');

    $.ajax({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
    type: "POST",
    url: url,
    data: JSON.stringify(event.data),
    dataType: "json"
    }).done(function(save_message) {
    alert(save_message.message);
    });
}
    