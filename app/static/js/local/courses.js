
function getSelectedCourse(elementId) {
   var selectedCourse = document.getElementById(elementId);
   
   if (selectedCourse.selectedIndex == -1)
      return null;
   
   return selectedCourse.options[selectedCourse.selectedIndex].text;
}

function specialTopicsName(){
   var courseTitle = getSelectedCourse('courseInfo');
   if (courseTitle === "---"){
      document.getElementById("submitAdd").disabled = true;
   }
   else{
      document.getElementById("submitAdd").disabled = false;
   }
   $(".specialTopics").remove();
   if (courseTitle != "---"){
      //The code below removes everything that isn't a number from the string
      var course = courseTitle.match(/\d/g).join("");
      //Then remove the numbers 86 from the string
      course = course.split("86").join("");
      console.log(course)
      if (course.length == 1){
         console.log("Made it into the conditional")
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

$(document).ready(function(){
    $('table').DataTable({paging: false});
});
