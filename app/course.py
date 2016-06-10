from allImports import *
from updateCourse import DataUpdate


@app.route("/courses/<tID>/<prefix>", methods=["GET", "POST"])
def courses(tID, prefix):
  username = authUser(request.environ)
  
  # These are the necessary components of the sidebar. Should we move them somewhere else?
  divisions = Division.select()
  programs = Program.select()
  subjects = Subject.select()
  
  # Checking the permissions of the user.
  # we need the subject to know if someone if a division chair or a program chair
  subject = Subject.get(Subject.prefix == prefix)
  users   = User.select(User.username, User.firstName, User.lastName)
  
  # Checking if person is division chair or program chair
  admin = User.get(User.username == username)
  divisionChair = DivisionChair.select().where(DivisionChair.username == username).where(DivisionChair.did == subject.pid.division.dID)
  programChair  = ProgramChair.select().where(ProgramChair.username == username).where(ProgramChair.pid == subject.pid.pID)
  
  terms = Term.select()
  print admin
  if (request.method == "GET"):
      
      print username
      
      # We need these for populating add course
      courseInfo = BannerCourses.select().where(BannerCourses.subject == prefix).order_by(BannerCourses.number)
      
      schedules = BannerSchedule.select()
      
      courses = Course.select().where(Course.prefix == prefix).where(Course.term == tID)
     
      instructors = {}
      for course in courses:
        instructors[course.cId] = InstructorCourse.select().where(InstructorCourse.course == course.cId)
      
      if admin.isAdmin or divisionChair.exists() or programChair.exists():
        return render_template("programAdmin.html",
                              cfg      = cfg,
                              courses = courses,
                              instructors = instructors,
                              programs = programs,
                              divisions = divisions,
                              subjects = subjects,
                              currentTerm = int(tID),
                              courseInfo = courseInfo,
                              users = users,
                              schedules = schedules,
                              allTerms = terms,
                              isAdmin  = admin.isAdmin
                            )

      else:
        return render_template("program.html",
                                cfg      = cfg,
                                courses = courses,
                                instructors = instructors,
                                programs = programs,
                                divisions = divisions,
                                subjects = subjects,
                                currentTerm = tID,
                                allTerms = terms
                              )
  if (request.method == "POST"):
    if admin.isAdmin or divisionChair.exists() or programChair.exists():
      page = request.path
      data   = request.form
      print data
      instructors = request.form.getlist('professors[]')
      newCourse = DataUpdate()
      cid = newCourse.addCourse(data, tID, instructors, prefix)
      if not newCourse.isTermEditable(tID):
        newCourse.addCourseChange(cid, prefix, "create")
      
      message = "Course: #{0} has been added".format(cid)
      log.writer("INFO", page, message)
      return redirect(url_for("courses", tID = tID, prefix = prefix))
    else:
      return render_template("404.html", cfg=cfg)