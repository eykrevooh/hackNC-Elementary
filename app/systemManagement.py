from allImports import *
from updateCourse import DataUpdate
import datetime


@app.route("/admin/systemManagement", methods=["GET", "POST"])
def systemManagement():
  if (request.method == "GET"):
      username = authUser(request.environ)
      admin = User.get(User.username == username)
      if admin.isAdmin:
         terms = Term.select()
         users = User.select()
         program = Program.get()
         today = datetime.date.today()
         return render_template("systemManagement.html",
                                 program       = program,
                                 cfg           = cfg,
                                 users         = users,
                                 terms         = terms,
                                 isAdmin       = admin.isAdmin,
                                 today         = today)