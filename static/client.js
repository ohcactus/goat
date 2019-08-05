$(document).ready(function() {
  $("#target").click(function() {
    alert("working");
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
             <img src="${x[3]}"/>
            </div>
         `);
    });
  });

  console.log("Here is hereweare on line 26", hereweare);

  $("#new-item-button").click(function(e) {
    e.preventDefault();
    var shoeName = $("#shoe_name").val();
    var shoePrice = $("#shoe_price").val();
    var form_data = new FormData($("#new-item")[0]);
    form_data.append("shoe_brand", shoeName);
    form_data.append("shoe_price", shoePrice);

    $.ajax({
      type: "POST",
      url: "/new_shoe",
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      success: function(data) {
        console.log(data)
      }
    });
  });
});
