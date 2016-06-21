function toggleArrowIcon(iconID,labelID) {
	console.log(iconID);
	console.log(labelID);
	$(iconID).toggleClass('glyphicon-menu-down');
	toggleLabel(labelID);
}

function toggleLabel(labelID) {
	$(labelID).parent().children('ul.tree').toggle(300);
}