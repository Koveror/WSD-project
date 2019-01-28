//This script is used for listening embedded games and acting accordingly.

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
    message = JSON.stringify(event.data);
    console.log("Received object: " + message);

    //FIXME: Can be moved up?
    setupAjax();

    if(event.data.messageType == "SAVE") {
        saveGame();
    } else if(event.data.messageType == "LOAD_REQUEST") {
        loadGame();
    } else if(event.data.messagetype == "SCORE") {
        submitScore();
    }
}

function setupAjax() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

//Save game state to database
function saveGame() {
    //Find the save form in the HTML to get a nicely formatted URL
    var form = $("#save_form");
    var url = form.attr('url');

    $.ajax({
    type: "POST",
    url: url,
    data: JSON.stringify(event.data),
    dataType: "json"
    }).done(function(save_message) {
    alert(save_message.message);
    });
}

//Load gameState from database and send it to the game
function loadGame() {

}

//Save score to the database
function submitScore() {

}
    