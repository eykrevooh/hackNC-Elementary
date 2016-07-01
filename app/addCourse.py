from allImports import *
from updateCourse import DataUpdate
from app.logic.NullCheck import NullCheck


@app.route("/addCourse/<tid>/<page>/", defaults={'prefix':0}, methods=["POST"])
@app.route("/addCourse/<tid>/<page>/<prefix>",methods=["POST"])
def addCourses(tid,page,prefix):
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if prefix != 0:
        subject = Subject.get(Subject.prefix == prefix)
        divisionChair = DivisionChair.select().where(DivisionChair.username == username).where(DivisionChair.did == subject.pid.division.dID)
        programChair  = ProgramChair.select().where(ProgramChair.username == username).where(ProgramChair.pid == subject.pid.pID)
    if admin.isAdmin or divisionChair.exists() or programChair.exists():
      current_page    = "/" + request.url.split("/")[-1]
      data            = request.form
      instructors     = request.form.getlist('professors[]')
      nullCheck       = NullCheck()
      values          = nullCheck.add_course_form(data)
      course = Course(bannerRef     = values['bannerRef'],
                  prefix            = values['prefix'],
                  term              = int(tid),
                  schedule          = values['schedule'],
                  capacity          = values['capacity'],
                  specialTopicName  = values['specialTopicName'],
                  notes             = data['requests'],
                  crossListed       = int(data['crossListed']),
                  rid               = values['rid']
                )
      course.save()
      cid = course.cId
      for professor in instructors:
        instructor = InstructorCourse(username = professor, course = course.cId)
        instructor.save()
        
      newCourse       = DataUpdate()
      if not newCourse.isTermEditable(tid):# IF THE TERM IS NOT EDITABLE
        newCourse.addCourseChange(cid, cfg["changeType"]["create"])     # ADD THE COURSE TO THE COURSECHANGE TABLE
      message = "Course: #{0} has been added".format(cid)
      log.writer("INFO", current_page, message)
      flash("Course has successfully been added!")
      if page == "courses":
        return redirect(url_for("courses", tID = str(tid), prefix = prefix))
      else:
          url = "courseManagement/" + page + "/" + str(tid)
          return redirect(url)
    else:
      return render_template("404.html", cfg=cfg)
    