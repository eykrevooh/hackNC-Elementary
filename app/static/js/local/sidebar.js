function toggleArrowIcon(element,ID) {
	$(element).toggleClass('glyphicon-menu-down');
	toggleID(ID);
}

function toggleID(ID) {
	$(ID).parent().children('ul.tree').toggle(300);
}