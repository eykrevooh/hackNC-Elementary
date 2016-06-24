from allImports import *
from updateCourse import DataUpdate


@app.route("/addCourse/<tid>/<page>/", defaults={'prefix':0}, methods=["POST"])
@app.route("/addCourse/<tid>/<page>/<prefix>",methods=["POST"])
def addCourses(tid,page,prefix):
    username = authUser(request.environ)
    subject = Subject.get(Subject.prefix == prefix)
    admin = User.get(User.username == username)
    if prefix != 0:
        divisionChair = DivisionChair.select().where(DivisionChair.username == username).where(DivisionChair.did == subject.pid.division.dID)
        programChair  = ProgramChair.select().where(ProgramChair.username == username).where(ProgramChair.pid == subject.pid.pID)
    if admin.isAdmin or divisionChair.exists() or programChair.exists():
      current_page    = "/" + request.url.split("/")[-1]
      data        = request.form
      instructors = request.form.getlist('professors[]')
      newCourse   = DataUpdate()
      cid         = newCourse.addCourse(data, tid, instructors, prefix)
    #   if not newCourse.isTermEditable(tID):     # If this is not an editable term
    #     newCourse.addCourseChange(cid, prefix, "create")    # Add the course to the special table
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
    