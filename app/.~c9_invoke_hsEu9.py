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
      changeTypes = ["create","update", "delete"]
      
      for term in terms:
        data[term] = {}
        for changeType in changeTypes:
          data[term][changeType] = CourseChange.select().where(CourseChange.term == term.termCode).where(CourseChange.changeType == changeType)

      """
      data = {
        Term : {
          ChangeType: [Course1, Course2, ..]
        }
      }
      """
      
      instructors = {}
      for course in courses:
        instructors[course.cId] = InstructorCourseChange.select().where(InstructorCourseChange.course == course.cId)
      
      
      return render_template("courseChange.html",
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
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if admin.isAdmin:
      data = request.form
      verify = DataUpdate()
      verify.verifyCourseChange(data)
      
      return redirect(url_for("courseChange"))