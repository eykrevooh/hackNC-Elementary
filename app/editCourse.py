from allImports import *
from updateCourse import DataUpdate
@app.route("/editcourse/<subject>", methods=["POST"])
def editcourse(subject):
  data = request.form
  professors = request.form.getlist('professors[]')
  editcourse = DataUpdate()
  editcourse.editCourse(data, subject, professors)
  return "hello"
  
  #Stop hating ishwar, lol