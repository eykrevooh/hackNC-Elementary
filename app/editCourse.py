from allImports import *
from updateCourse import DataUpdate

@app.route("/editCourseModal/<tid>/<prefix>/<cid>", methods=["GET"])
def editCourseModal(tid, prefix, cid):
  checkUser = DataUpdate()
  if checkUser.checkUserLevel(prefix):
    
    # Select all schedules
    schedules = BannerSchedule.select()
    # Select all terms
    terms = Term.select()
    # Select the course informations
    course = Course.get(Course.cId == cid)
    # Select all users
    users = User.select()
    # Select instructors for the course
    instructors = {}
    instructors[course.cId] = InstructorCourse.select().where(InstructorCourse.course == course.cId)
    
    return render_template("editCourse.html",
                            schedules = schedules,
                            cfg = cfg,
                            terms     = terms,
                            course    = course,
                            users = users,
                            instructors = instructors,
                            currentTerm = tid
                            )

@app.route("/editcourse/<tid>/<prefix>", methods=["POST"])
def editcourse(tid, prefix):
  data = request.form
  professors = request.form.getlist('professors[]')
  editcourse = DataUpdate()
  editcourse.editCourse(data, prefix, professors)
  return redirect(url_for("courses", tID=tid, prefix=prefix))
  
  #Stop hating ishwar, lol