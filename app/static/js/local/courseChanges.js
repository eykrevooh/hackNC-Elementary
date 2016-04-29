$('#verifyCourseChange').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var id = button.data('id') // Extract info from data-id
  var modal = $(this)
  modal.find('#courseChangeId').val(id)
});