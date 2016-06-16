$(document).ready(function () {
	$('label.tree-toggler').click(function () {
		$(this).parent().children('ul.tree').toggle(300);
	});
	
	$('span.glyphicon').click(function(){
		$(this).toggleClass('glyphicon-menu-down')
	})
});

