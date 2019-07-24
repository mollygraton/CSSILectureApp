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

      //update the chart

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

function fetchCurrentChart() {
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

      //update the chart

      // Start the timer again for the next request.
      startTimer(10000)
    })
}
function drawChart() {

    // Create the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Understanding');
    data.addColumn('number', 'Students');
    total1 = {{numOf1}}
    total2 = {{numOf2}}
    total3 = {{numOf3}}
    total4 = {{numOf4}}
    total5 = {{numOf5}}
    data.addRows([
      ['1', total1],
      ['2', total2],
      ['3', total3],
      ['4', total4],
      ['5', total5]
    ]);

    var options = {'title':'General Class Comprehension'};
    var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
    chart.draw(data, options);
  }
