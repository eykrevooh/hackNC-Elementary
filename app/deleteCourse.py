from allImports import *
from updateCourse import DataUpdate
@app.route("/deletecourse/<term>/<prefix>", methods=["POST"])
def deletecourse(prefix, term):
  page = "/" + request.url.split("/")[-1]
  username = authUser(request.environ)
  
  admin = User.get(User.username == username)
  
  ## We need subject to check if the user is a program or division chair. 
  subject = Subject.get(Subject.prefix == prefix)
  
  ## Check to see if the user is a program or divison chair.
  divisionChair = DivisionChair.select().where(DivisionChair.username == username).where(DivisionChair.did == subject.pid.division.dID)
  programChair  = ProgramChair.select().where(ProgramChair.username == username).where(ProgramChair.pid == subject.pid.pID)
  
  if admin.isAdmin or divisionChair.exists() or programChair.exists():
    data = request.form
    deleteCourse = DataUpdate()
    created = deleteCourse.addCourseChange(int(data['cid']), prefix, "delete")
    if not created:
      deleteCourse.editCourseChange(int(data['cid']), prefix, "delete")
    message = "Course: course {} has been deleted".format(data['cid'])
    log.writer("INFO", page, message)
    deleteCourse.deleteCourse(data, prefix)
    return redirect(url_for("courses", tID = term, prefix = prefix))