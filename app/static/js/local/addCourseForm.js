/*global $*/
$("#showForm").click(function() {
   $("#createCourseFormJumbo").css('display', 'block');
   $(this).hide();
});

$("#hideForm").click(function() {
     $("#createCourseFormJumbo").css('display', 'none');
     $("#showForm").show();
});

var infoLabel = '<div class="form-group col-xs-12 notice alert alert-warning alert-dismissible" role="alert">\
                <p>Choosing a room does not guarantee that the room will assigned</p>\
              </div>';

$("#roomSelect").on('changed.bs.select', function(e) {
 var selectedOption= $('#roomSelect').find(":selected").text();
 console.log(selectedOption)
 if(selectedOption != '---'){
     if(!($('.notice')[0])){
  $("#notesText").before(infoLabel);
     }
 } else {
    $(".notice").remove();
 }
});


$('select').change(function(){
    alert($(this).prev().prop('nodeName'));
    $(this).css('text-color', 'pink');
});


    var $window = $(window),
        $forms = $('.offset_input');

    function resize() {
        if ($window.width() < 992) {
            return $forms.removeClass('right');
        }

        $forms.addClass('right');
    }

    $window
        .resize(resize)
        .trigger('resize');

