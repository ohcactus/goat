$(document).ready(function() {
    $("#search").on("change paste keyup", function() {
        var whatTheyTyped = $(this).val();
        $.get("/search_item", {searchitem: whatTheyTyped}, function(data) {
            data = JSON.parse(data);
            console.log(data);
            $("#all-shoes-of-search").html("");
            data.forEach(x => {
                $("#all-shoes-of-search").append(`
                       <div class="shoe-container">
                       <div class="shoe-name">${x[1]}</div>
                       <div>${x[2]}</div>
                       <img src="${x[3]}"/>
                      </div>
                   `);
              });
          });
     });
});
  