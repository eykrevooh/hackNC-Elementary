$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    this.innerHTML = (this.innerHTML == 'Close Sidebar') ? 'Open Sidebar' : 'Close Sidebar' ;
});