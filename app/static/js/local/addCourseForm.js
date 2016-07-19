$("#showForm").click(function() {
   $("#createCourseFormJumbo").css('display', 'block');
   $(this).hide();
});

$("#hideForm").click(function() {
     $("#createCourseFormJumbo").css('display', 'none');
     $("#showForm").show();
});

var infoLabel = '<div class="notice alert alert-warning alert-dismissible" role="alert">\
                <p>Choosing a room does not guarantee that the room will assigned</p>\
              </div>';

$("#roomSelect").on('shown.bs.select', function(e) {
  $("#createFormContainer").append(infoLabel);
});

$("#roomSelect").on("hidden.bs.select", function(e) {
    $(".notice").remove();
})