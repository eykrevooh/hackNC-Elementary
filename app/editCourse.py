from allImports import *
from updateCourse import DataUpdate

@app.route("/editCourseModal/<tid>/<prefix>/<cid>/<page>", methods=["GET"])
def editCourseModal(tid, prefix, cid, page):
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
    # SELECT ALL ROOMS
    rooms     = Rooms.select()
    return render_template("snips/editCourse.html",
                            schedules = schedules,
                            cfg = cfg,
                            terms     = terms,
                            course    = course,
                            users = users,
                            instructors = instructors,
                            currentTerm = int(tid),
                            page        = page,
                            rooms       = rooms
                            )

@app.route("/editcourse/<tid>/<prefix>/<page>", methods=["POST"])
def editcourse(tid, prefix, page):
  page1 =  "/" + request.url.split("/")[-1]
  data = request.form
  professors = request.form.getlist('professors[]')
  editcourse = DataUpdate()
  
  if not editcourse.isTermEditable(tid):
      created = editcourse.addCourseChange(data['cid'], prefix, "update")
      
  editcourse.editCourse(data, prefix, professors)
  message = "Course: course {} has been edited".format(data['cid'])
  log.writer("INFO", page1, message)
  flash("Course information has successfully been modified!")
  if page == 'courses':
    return redirect(url_for("courses", tID=tid, prefix=prefix))
  else:
    url = "/courseManagement/" + page + "/" + tid
    return redirect(url)
  
  #Stop hating ishwar, lol