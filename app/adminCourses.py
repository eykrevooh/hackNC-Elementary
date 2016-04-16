from allImports import *


@app.route("/admin/courses/<tID>/<prefix>", methods=["GET", "POST"])
def adminCourses(tID, prefix):
  if (request.method == "GET"):
      username = authUser(request.environ)
      admin = User.get(User.username == username)
      if admin.isAdmin == False:
        return redirect(url_for("courses", tID = tID, prefix = prefix))
      
      # These are the necessary components of the sidebar. Should we move them somewhere else?
      divisions = Division.select()
      programs = Program.select()
      subjects = Subject.select()
      
      courses = Course.select().where(Course.prefix == prefix).where(Course.term == tID)
      
      instructors = {}
      for course in courses:
        instructors[course.cId] = InstructorCourse.select().where(InstructorCourse.course == course.cId)
      
        
      return render_template("programAdmin.html",
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
  