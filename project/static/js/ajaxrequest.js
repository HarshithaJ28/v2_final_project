document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM LOADED");

    var requestinfo = document.getElementById('requestinfo');

    var eventSource = new EventSource('/stream');

    eventSource.onmessage = function(event) {
        var data = event.data;
        console.log("MESSAGEEEEE")
        var p = document.createElement('p');
        p.innerHTML = "<span class=red>[*]</span> " + data;
        requestinfo.appendChild(p);
    };

    eventSource.onerror = function(event) {
        console.error("Error occurred with SSE connection.");
        eventSource.close();
    };
});
