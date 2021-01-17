async function getResults(imdb_url, location_code) {
    console.log("Querying " + imdb_url);
    const response = await fetch("check_imdb_list",
        {
            method: "POST",
            body: JSON.stringify({ url: imdb_url, location_code: location_code }),
            headers: { 'Content-Type': 'application/json' }
        });
    task = await response.json();
    return task
}


function doPoll(task_id) {

    //console.log("Polling task: " + task_id)

    $.ajax({
        type: "POST",
        url: 'get_state',
        data: JSON.stringify({"task_id": task_id}),
        success: async function (data) {
            
            //console.log(task_id + ": " + data)

            switch (data.state) {

                case "SUCCESS":
                    const response = await fetch("get_result",
                    {
                        method: "POST",
                        body: JSON.stringify({"task_id": task_id}),
                        headers: { 'Content-Type': 'application/json' }
                    });
                    resp_json = response.json().then(data => renderTable('result_area', data));
                    break;
                
                case "PENDING":
                    $("#progress_text").html("Submitting...");
                    setTimeout(doPoll, 1000, task_id);
                    break;
                
                case "PROGRESS":
                    $("#progress_text").html(data.message);
                    setTimeout(doPoll, 1000, task_id);
                    break;

                default:
                    // failure
                    fillResultsArea('</br><img src="static/assets/error.png" width="50" alt=""></br></br><p>'+ data.message + '<br/>Please try again or <a href="/contact">✉️ contact</a> me!</p>');
                    break;

            }
        },
        contentType: 'application/json',
    });
}

function fillResultsArea(html_content) {
    
    $("#result_area").html(html_content);
}

$("#check_button").bind("click", function () {
    fillResultsArea('<div class="lds-facebook"><div></div><div></div><div></div></div><p id="progress_text">Can take a few minutes ...</p>');

    // get watchlist URL
    imdb_url = $("#url_input").val();
    imdb_url = imdb_url.trim()

    // get location code
    location_code = $("#location_code_selector").val();

    getResults(imdb_url, location_code).then(task => doPoll(task.task_id));
});

$("#send_message_button").bind("click", async function () {

    // get watchlist URL
    name = $("#contactName").val();
    email = $("#contactEMail").val();
    reason = $("#contactReason").val();
    text = $("#contactMessage").val();

    if (name == null || name == "", reason == null || reason == "", text == null || text == "") {
        alert("Please fill all required fields!");
        return false;
      }

    message = {
        "name": name,
        "email": email,
        "reason": parseInt(reason),
        "message": text,
        "timestamp": new Date().toISOString()
    };

    const response = await fetch("send_message",
        {
            method: "POST",
            body: JSON.stringify(message),
            headers: { 'Content-Type': 'application/json' }
        });
    task = await response.json();

    alert("❤️ Thanks!");
    
    $("#send_message_button").prop("disabled", true);
});
