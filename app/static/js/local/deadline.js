// Every HTML page should have a complimentary JS file, 
// even if it's empty
$('#editDeadline').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var id = button.data('id')
  var description = button.data('description')
  // Update the modal's content
  var modal = $(this)
  modal.find('#deadlineid').val(id)
  modal.find('#deadlineDescription').val(description) 
});

$('#deleteDeadline').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var id = button.data('id') // Extract info from data-id
  var modal = $(this)
  modal.find('#deadlineid').val(id)
});


$('.deadlineEditTextarea').on('change keyup keydown paste cut', function(e){
    var that = $(this);
    while (that.scrollTop()) {
        $(this).height(function(i,h){
            return h + 20;
        });
    }
});
