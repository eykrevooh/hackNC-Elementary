from allImports import *
from updateCourse import DataUpdate
@app.route("/deletecourse/<tid>/<prefix>/<page>", methods=["POST"])
def deletecourse(prefix, tid, page):
  #DATA NEEDED FOR MANIPULATION
  current_page = "/" + request.url.split("/")[-1]
  username = authUser(request.environ)
  tdcolors = 'danger,danger,danger,danger,danger'
  dataUpdateObj = DataUpdate()
  data = request.form
  cid = int(data['cid'])
  #START PROCESSING THE DELETION OF THE COURSE
  course = Course.get(Course.cId == cid)
  #MAKE SURE THE USER HAS THE CORRECT RIGHTS TO DELETE A COURSE
  if dataUpdateObj.checkUserLevel(course.prefix): 
    if not dataUpdateObj.isTermEditable(tid):
      change = CourseChange.select().where(CourseChange.cId==cid)
      #IF THE RECORD ALREADY EXSISTED THEN WE NEED TO UPDATE THE INFORMATION
      if change.exists(): 
        updateRecord = CourseChange.get(CourseChange.cId==cid)
        updateRecord.changeType = cfg["changeType"]["delete"]
        updateRecord.tdcolors   = tdcolors
        updateRecord.lastEditBy = username 
        updateRecord.save()
      else:
        dataUpdateObj.addCourseChange(course.cId,cfg["changeType"]['delete'])
    instructors = InstructorCourseChange.select().where(InstructorCourseChange.course == cid)
    for instructor in instructors:
        instructor.delete_instance()
    course.delete_instance()
    
  flash("Course has been successfully deleted")
    
  if page == 'courses':
    return redirect(url_for("courses", tID=tid, prefix=prefix))
  else:
    url = "courseManagement/" + page + "/" + tid
    return redirect(url)