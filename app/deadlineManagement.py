from allImports import *
from updateCourse import DataUpdate
import datetime


@app.route("/deadline/create", methods=[ "POST"])
def deadlineCreate():
   username = authUser(request.environ)
   admin = User.get(User.username == username)
   if admin.isAdmin:
        data = request.form
        deadline = Deadline(term = data['term'], description=data['deadlineDescription'], date=data['deadlineDate'])
        deadline.save()
        
        flash("Your Deadline has been created")
   return redirect(url_for("systemManagement"))
   
   
@app.route("/deadline/edit", methods=[ "POST"])
def deadlineEdit():
   username = authUser(request.environ)
   admin = User.get(User.username == username)
   if admin.isAdmin:
        data = request.form
        deadline = Deadline.get(Deadline.id == data['id'])
        deadline.description = data['deadlineDescription']
        print deadline.description 
        deadline.save()
        
        flash("Your Deadline has been edited")
   return redirect(url_for("deadlineDisplay"))