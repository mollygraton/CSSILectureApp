const note_div = document.querySelector('#chat_div2')

function startTimer(timeoutPeriod) {
  setTimeout(fetchCurrentNote, timeoutPeriod)
}

// Ask the server for the current note immediately.
function fetchCurrentNote() {
  fetch('/ajax/get_current_chat')
    .then(function(response) {
      return response.json()
    })
    .then(function (myJson) {
      // Update the div.
      var stringFun = ""
      note_div.innerHTML = ""
      for(x=0;x<myJson.question.length;x++){
        stringFun += `<input type="checkbox" name="to_delete" value="${myJson.question[x].key}">${myJson.question[x].question_text}</br>`
      }
      stringFun += `<input type="submit" name="" value="Delete Selected"></input>`
      note_div.innerHTML = stringFun
      // Start the timer again for the next request.
      startTimer(10000)
    })
}





if (note_div != null) {
  // If note_div is null it means that the user is not logged in.  This is
  // because the jinja template for the '/' handler only renders this div
  // when the user is logged in.  Querying for a node that does not exist
  // returns null.

  // Start by fetching the current note without any delay.
  fetchCurrentNote()
}
