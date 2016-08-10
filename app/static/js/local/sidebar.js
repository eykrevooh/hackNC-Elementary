/* global $ */

$('.first-level').on('click', function(){
   $(this).children().toggleClass('glyphicon-chevron-down');
   $(this).children().toggleClass('glyphicon-chevron-up');
});