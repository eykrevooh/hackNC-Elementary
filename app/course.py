from allImports import *
from updateCourse import DataUpdate


@app.route("/courses/<tID>/<prefix>", methods=["GET", "POST"])
def courses(tID, prefix):
  if (request.method == "GET"):
      username = authUser(request.environ)
      admin = User.get(User.username == username)
      print username
      
      
      # These are the necessary components of the sidebar. Should we move them somewhere else?
      divisions = Division.select()
      programs = Program.select()
      subjects = Subject.select()
      
      terms = Term.select()
      
      
      # we need the subject to know if someone if a division chair or a program chair
      subject = Subject.get(Subject.prefix == prefix)
      users   = User.select(User.username, User.firstName, User.lastName)
       # We need these for populating add course
      courseInfo = BannerCourses.select().where(BannerCourses.subject == prefix).order_by(BannerCourses.number)
      
      schedules = BannerSchedule.select()
      
      # Checking if person is division chair or program chair
      divisionChair = DivisionChair.select().where(DivisionChair.username == username).where(DivisionChair.did == subject.pid.division.dID)
      programChair  = ProgramChair.select().where(ProgramChair.username == username).where(ProgramChair.pid == subject.pid.pID)
      
      
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
  data   = request.form
  instructors = request.form.getlist('professors[]')
  
  newCourse = DataUpdate()
  newCourse.addCourse(data, tID, instructors, prefix)
  return redirect(url_for("courses", tID = tID, prefix = prefix))