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
  
  
  #THIS IS SO THAT WE CAN HAVE THE NAME OF THE PROGRAM AS A HEADER ON THE TOP OF EVERY PAGE
  currentProgram = Program.select().where(Program.pID     == subject.pid,
                                          subject.prefix  == prefix).get()
                                                      
  
 
  
  # Checking if person is division chair or program chair
  admin = User.get(User.username == username)
  divisionChair = DivisionChair.select().where(DivisionChair.username == username).where(DivisionChair.did == subject.pid.division.dID)
  programChair  = ProgramChair.select().where(ProgramChair.username == username).where(ProgramChair.pid == subject.pid.pID)
  terms = Term.select()

  if (request.method == "GET"):
      
      # We need these for populating add course
      courseInfo = BannerCourses.select().where(BannerCourses.subject == prefix).order_by(BannerCourses.number)
      
      schedules = BannerSchedule.select()
      
      courses = Course.select().where(Course.prefix == prefix).where(Course.term == tID)
     
      instructors = {}
      for course in courses:
        instructors[course.cId] = InstructorCourse.select().where(InstructorCourse.course == course.cId)
      
      if admin.isAdmin or divisionChair.exists() or programChair.exists():
        return render_template("programAdmin.html",
                              cfg             = cfg,
                              courses         = courses,
                              instructors     = instructors,
                              programs        = programs,
                              divisions       = divisions,
                              subjects        = subjects,
                              currentTerm     = int(tID),
                              courseInfo      = courseInfo,
                              users           = users,
                              schedules       = schedules,
                              allTerms        = terms,
                              isAdmin         = admin.isAdmin,
                              isProgramChair  = divisionChair.exists(),
                              isDivisionChair = programChair.exists(),
                              currentProgram  = currentProgram
                            )
      else:
        return render_template("program.html",
                                cfg           = cfg,
                                courses       = courses,
                                instructors   = instructors,
                                programs      = programs,
                                divisions     = divisions,
                                subjects      = subjects,
                                currentTerm   = int(tID),
                                allTerms      = terms,
                                currentProgram = currentProgram
                              )
  if (request.method == "POST"):
    if admin.isAdmin or divisionChair.exists() or programChair.exists():
      page = request.path
      data   = request.form
      if data["schedule"] == "":
        schedule = None
      else:
        schedule = data["schedule"]
      print "Data is {0}".format(data)
      instructors = request.form.getlist('professors[]')
      newCourse = DataUpdate()
      cid = newCourse.addCourse(data, tID, instructors, prefix, schedule)
      if not newCourse.isTermEditable(tID):     # If this is not an editable term
        newCourse.addCourseChange(cid, prefix, "create")    # Add the course to the special table
      
      message = "Course: #{0} has been added".format(cid)
      log.writer("INFO", page, message)
      return redirect(url_for("courses", tID = tID, prefix = prefix))
    else:
      return render_template("404.html", cfg=cfg)