from allImports import *


@app.route("/courses/<tID>/<prefix>", methods=["GET", "POST"])
def courses(tID, prefix):
  if (request.method == "GET"):
      divisions = Division.select()
      programs = Program.select()
      subjects = Subject.select()
      
      subject = Subject.get(Subject.prefix == prefix)
      courses = Course.select().where(Course.prefix == prefix).where(Course.term == tID)
      
      instructors = {}
      for course in courses:
        instructors[course.cId] = InstructorCourse.select().where(InstructorCourse.course == course.cId)
      
      username = authUser(request.environ)
      print username
      # admin = User.select(User.isAdmin).where(User.username == username)
      admin = User.get(User.username == username)
      divisionChair = DivisionChair.select().where(DivisionChair.username == username).where(DivisionChair.did == subject.pid.division.dID)
      programChair = ProgramChair.select().where(ProgramChair.username == username)
      if admin.isAdmin:
        print "isAdmin: True"
      elif divisionChair.exists():
        print "we are here division chair"
        return render_template("programAdmin.html",
                              cfg      = cfg,
                              courses = courses,
                              instructors = instructors,
                              programs = programs,
                              divisions = divisions,
                              subjects = subjects,
                              term = tID
                            )
      elif programChair.exists():
        print("we are here")
        return render_template("programAdmin.html",
                              cfg      = cfg,
                              courses = courses,
                              instructors = instructors,
                              programs = programs,
                              divisions = divisions,
                              subjects = subjects,
                              term = tID
                            )
      else:
        print 'false'
        
      return render_template("program.html",
                              cfg      = cfg,
                              courses = courses,
                              instructors = instructors,
                              programs = programs,
                              divisions = divisions,
                              subjects = subjects,
                              term = tID
                            )
  data   = request.form
  termId = data["termSelect"]
  return "hello"
  