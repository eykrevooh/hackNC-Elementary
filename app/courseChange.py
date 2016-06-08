from allImports import *
from updateCourse import DataUpdate


@app.route("/courses/changes", methods=["GET"])
def courseChange():
  if (request.method == "GET"):
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if admin.isAdmin:
      
      data = {}
      terms = Term.select().where(Term.editable == False)
      courses = CourseChange.select()
      courseList = []
      
      for term in terms:
        coursesHistory = CourseChange.select().where(CourseChange.term == term.termCode).where(CourseChange.verified == False)
        for courseHistory in coursesHistory:
          courseInfo = []
          
          
          if courseHistory.changeType == 'delete':
            for i in range(5):
              courseInfo.append('delete')
            course = courseHistory
            
          
          if courseHistory.changeType == 'create':
            for i in range(5):
              courseInfo.append('create')
            course = Course.get(Course.cId == courseHistory.cId)

          if courseHistory.changeType == 'update':
            course = Course.get(Course.cId == courseHistory.cId)
            
            courseInfo.append(None)
            
            # compare the instructors in old and new table
            oldInstructors = []
            newInstructors = []
            
            newInstructor = (InstructorCourse.select()
                                             .where(InstructorCourse.course == course.cId))
                                            
            oldInstructor = (InstructorCourseChange.select()
                                            .where(InstructorCourseChange.course == course.cId))
            
            for instructor in newInstructor:
              newInstructors.append(instructor.username.username)
            for instructor in oldInstructor:
              oldInstructors.append(instructor.username.username)
            
            if set(oldInstructors) == set(newInstructors):
              courseInfo.append('update')
            else:
              courseInfo.append(None)
            
            # compare the schedule in old and new table
            if courseHistory.schedule != course.schedule:
              courseInfo.append('update')
            else:
              courseInfo.append(None)
            
            # compare the capacity
            if courseHistory.capacity != course.capacity:
              courseInfo.append('update')
            else:
              courseInfo.append(None)
            
            #compare the notes
            if courseHistory.notes != course.notes:
              courseInfo.append('update')
            else:
              courseInfo.append(None)

          courseList.append((courseInfo, course))
          data[term] = courseList
      
      
      

      """
      data = {
        Term : {[class, class, class, class],
                
           ]
        }
      }
      """
      
      instructors = {}
      for course in courses:
        instructors[course.cId] = InstructorCourseChange.select().where(InstructorCourseChange.course == course.cId)
      
      
      return render_template("courseChange.html",
                              courseList  = courseList,
                              cfg         = cfg,
                              data        = data,
                              instructors = instructors,
                              isAdmin     = admin.isAdmin
                            )
    else:
      return render_template("404.html", cfg=cfg)
  
@app.route("/courses/changes/verified", methods=["POST"])
def verifycourseChange():
  if (request.method == "POST"):
    page = request.path
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if admin.isAdmin:
      data = request.form
      verify = DataUpdate()
      verify.verifyCourseChange(data)
      message = "Course Change: {0} has been verified".format(data['id'])
      log.writer("INFO", page, message)
      flash("Your course has been marked verified")
      return redirect(url_for("courseChange"))