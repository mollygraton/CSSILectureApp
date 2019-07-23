const current_chat = document.querySelector('#chat')

function startTimer() {
  const microseconds = 2000  // 2 seconds
  window.setTimeout(fetchCurrentChat, microseconds)
}

// Ask the server for the current note immediately.
function fetchCurrentChat() {
  fetch('/ajax/get_current_chat')
    .then(function(response) {
      return response.json()
    })
    .then(function (myJson) {
      // Update the div.
      chat_div.innerHTML = myJson.current_chat

      // Start the timer again for the next request.
      startTimer()
    })
}

//if (current_chat != null) {
  // If note_div is null it means that the user is not logged in.  This is
  // because the jinja template for the '/' handler only renders this div
  // when the user is logged in.  Querying for a node that does not exist
  // returns null.

  // Start by fetching the current note without any delay.
  fetchCurrentChat()
//}
