from allImports import *
from updateCourse import DataUpdate
import datetime


@app.route("/", methods=["GET", "POST"])
def deadlineDisplay():
   if (request.method == "GET"):
      username = authUser(request.environ)
      admin = User.get(User.username == username)
      dates = Deadline.select(Deadline.date).distinct().order_by(Deadline.date)
      deadlines = []
      for date in dates:
         deadlines.append((date.date, Deadline.select().where(Deadline.date == date.date)))
      print deadlines
      
      today = datetime.date.today()
         
   return render_template("deadline.html",
                           cfg = cfg,
                           isAdmin = admin.isAdmin,
                           deadlines = deadlines,
                           today = today)