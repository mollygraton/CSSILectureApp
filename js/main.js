const allow_input = document.querySelector('#allow_input')

function startTimer() {
  const microseconds = 2000  // 2 seconds
  window.setTimeout(fetchInputAllow, microseconds)
}

// Ask the server for the current note immediately.
function fetchInputAllow() {
  fetch('/ajax/get_current_node')
    .then(function(response) {
      return response.json()
    })
    .then(function (myJson) {
      // Update the div.
      note_div.innerHTML = myJson.note

      // Start the timer again for the next request.
      startTimer()
    })
}

if (allow_input != null) {
  // If note_div is null it means that the user is not logged in.  This is
  // because the jinja template for the '/' handler only renders this div
  // when the user is logged in.  Querying for a node that does not exist
  // returns null.

  // Start by fetching the current note without any delay.
  fetchInputAllow()
}
