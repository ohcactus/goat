$(document).ready(function() {
  $("#target").click(function() {
    alert("Handler for .click() called.");
  });

  var hereweare;
  $.get("/get_shoes", function(data) {
    data = JSON.parse(data);
    data.forEach(x => {
      console.log(x);
      $("#all-shoes").append(`
             <div class="shoe-container">
             <div class="shoe-name">${x[1]}</div>
             <div>${x[2]}</div>
            </div>
         `);
    });
  });

  console.log("Here is hereweare on line 26", hereweare);
});
