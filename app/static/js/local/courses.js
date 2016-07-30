
function getSelectedCourse(elementId) {
   var selectedCourse = document.getElementById(elementId);
   
   if (selectedCourse.selectedIndex == -1)
      return null;
   
   return selectedCourse.options[selectedCourse.selectedIndex].text;
}

function specialTopicsName(){
   var courseTitle = getSelectedCourse('courseInfo');
   //DO THE WORK TO DISABLE AND ABLE THE BUTTON
   if (courseTitle === "---"){
      document.getElementById("submitAdd").disabled = true;
      document.getElementById("submitAdd").className = "btn btn-default btn"; 
   }
   else{
      document.getElementById("submitAdd").disabled = false;
      document.getElementById("submitAdd").className = "btn btn-success btn"; 
   }
   //THEN DO THE WORK FOR SPECIAL TOPICS NAMES
   $(".specialTopics").remove();
   console.log(courseTitle)
   if (courseTitle != "---"){
      var course = courseTitle.split(" ", 2);
      var courseNum = parseInt(course[1], 10);
      if ((courseNum % 100) == 86){
         $('#courseSelect').append('<input onchange="changeInput()" type="text" id="specialTopics" class="form-control specialTopics" placeholder="enter special topics name" value=""/>')
      }
   }
}

function changeInput(){
   $('#specialTopicsName').remove();
   var text = document.getElementById('specialTopics').value;
   console.log(text);
   $('#addCourseForm').append('<input type="hidden" id="specialTopicsName" name="specialTopicName" value="'+text+'" />')
   console.log("changeInput happened")
}

$(document).ready(function(){
    $('[data-toggle="popover"]').popover({
        placement : 'top'
    });
    
});


// $(function() {

//     $('#side-menu').metisMenu();

// });

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
// $(function() {
//     $(window).bind("load resize", function() {
//        var topOffset = 50;
//        var width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
//        if (width < 768) {
//             $('div.navbar-collapse').addClass('collapse');
//             topOffset = 100; // 2-row-menu
//        } else {
//             $('div.navbar-collapse').removeClass('collapse');
//        }

//        var height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
//        height = height - topOffset;
//        if (height < 1) height = 1;
//        if (height > topOffset) {
//             $("#page-wrapper").css("min-height", (height) + "px");
//        }
//     });

//     var url = window.location;
//     // var element = $('ul.nav a').filter(function() {
//     //     return this.href == url;
//     // }).addClass('active').parent().parent().addClass('in').parent();
//     var element = $('ul.nav a').filter(function() {
//     return this.href == url;
//     }).addClass('active').parent();

//     while(true){
//        if (element.is('li')){
//             element = element.parent().addClass('in').parent();
//        } else {
//             break;
//        }
//     }
// });