$(document).ready(function() {
    $.get("/get_shoes_of_user", function(data) {
        data = JSON.parse(data);
        data.forEach(x => {
          console.log(x);
          $("#all-shoes-of-user-sell").append(`
                 <div class="shoe-container">
                 <div class="shoe-name">${x[1]}</div>
                 <div>${x[2]}</div>
                 <img src="${x[3]}"/>
                </div>
             `);
        });
      });
});
  