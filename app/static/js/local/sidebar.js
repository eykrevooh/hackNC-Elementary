function toggleArrowIcon(element,ID) {
	console.log("Inside of the toggleArrowIcon function:")
	console.log(element)
	console.log(ID)
	$(element).toggleClass('glyphicon-menu-down');
	toggleID(ID);
}

function toggleID(ID) {
	console.log("Inside of the toggleID function:")
	console.log(ID)
	$(ID).parent().children('ul.tree').toggle(300);
}