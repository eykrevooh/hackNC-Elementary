from allImports import *
from updateCourse import DataUpdate
import datetime


@app.route("/deadline/create", methods=[ "POST"])
def deadlineCreate():
   page = request.path
   username = authUser(request.environ)
   admin = User.get(User.username == username)
   if admin.isAdmin:
        data = request.form
        deadline = Deadline(term = data['term'], description=data['deadlineDescription'], date=data['deadlineDate'])
        deadline.save()
        message = "Deadline: {0} has been added".format(deadline.description)
        log.writer("INFO", page, message)
        flash("Your Deadline has been created")
   return redirect(url_for("systemManagement"))
   
   
@app.route("/deadline/edit", methods=[ "POST"])
def deadlineEdit():
   page = request.path
   username = authUser(request.environ)
   admin = User.get(User.username == username)
   if admin.isAdmin:
        data = request.form
        deadline = Deadline.get(Deadline.id == data['id'])
        deadline.description = data['deadlineDescription']
        deadline.save()
        message = "Deadline: has been edited to {0}".format(deadline.description)
        log.writer("INFO", page, message)
        flash("Your Deadline has been edited")
   return redirect(url_for("deadlineDisplay"))
   
@app.route("/deleteDeadline", methods=["POST"])
def deleteDeadline():
   page = request.path
   username = authUser(request.environ)
   admin = User.get(User.username == username)
   if admin.isAdmin:
      data = request.form
      deadline = Deadline.get(Deadline.id == int(data['id']))
      deadline.delete_instance()
      message = "Deadline: {0} has been deleted".format(deadline.description)
      log.writer("INFO", page, message)
      flash("Your Deadline has been deleted")
   return redirect(url_for("deadlineDisplay"))