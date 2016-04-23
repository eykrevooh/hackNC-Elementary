from allImports import *
from updateCourse import DataUpdate
@app.route("/deletecourse/<term>/<subject>", methods=["POST"])
def deletecourse(subject, term):
  username = authUser(request.environ)
  admin = User.get(User.username == username)
  if admin.isAdmin:
    data = request.form
    deletecourse = DataUpdate()
    deletecourse.deleteCourse(data, subject)
    return redirect(url_for("courses", tID = term, prefix = subject))