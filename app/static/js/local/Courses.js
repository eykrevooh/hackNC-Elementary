
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


