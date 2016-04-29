from allImports import *
from updateCourse import DataUpdate
@app.route("/deletecourse/<term>/<subject>", methods=["POST"])
def deletecourse(subject, term):
  page = request.path
  username = authUser(request.environ)
  admin = User.get(User.username == username)
  if admin.isAdmin:
    data = request.form
    deleteCourse = DataUpdate()
    created = deleteCourse.addCourseChange(int(data['cid']), subject, "delete")
    if not created:
      deleteCourse.editCourseChange(int(data['cid']), subject, "delete")
    message = "Course: course {} has been deleted".format(data['cid'])
    log.writer("INFO", page, message)
    deleteCourse.deleteCourse(data, subject)
    return redirect(url_for("courses", tID = term, prefix = subject))