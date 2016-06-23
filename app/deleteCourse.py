from allImports import *
from updateCourse import DataUpdate
@app.route("/deletecourse/<tid>/<prefix>/<page>", methods=["POST"])
def deletecourse(prefix, tid, page):
  current_page = "/" + request.url.split("/")[-1]
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
    deleteCourse.deleteCourse(data, prefix)
    if page == 'courses':
      return redirect(url_for("courses", tID=tid, prefix=prefix))
    else:
      url = "courseManagement/" + page + "/" + tid
      return redirect(url)