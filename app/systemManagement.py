from allImports import *
from updateCourse import DataUpdate
import datetime 


@app.route("/admin/systemManagement", methods=["GET", "POST"])
def systemManagement():
  if (request.method == "GET"):
      username = authUser(request.environ)
      admin = User.get(User.username == username)
      if admin.isAdmin:
         terms          = Term.select()
         termSemesters  = Term.select(Term.semester).distinct()
         users          = User.select()
         program        = Program.get()
         today          = datetime.date.today()
         
         #WE WANT THE USER TO HAVE THE ABILITY TO SELECT A YEAR AGO AND THREE YEARS PAST THE CURRENT YEAR
         years       = []
         year  = int(time.strftime("%Y")) - 1   #START WITH ONE YEAR AGO
         for x in range(5):
            if x == 0:
               years.append(str(year))          #APPEND THE ONE YEAR AGO
            else:
               year += 1
               years.append(str(year))          #APPEND CURRENT NUMBER PLUS ONE
         
         return render_template("systemManagement.html",
                                 terms          = terms,
                                 termSemesters  = termSemesters,
                                 years          = years,
                                 program        = program,
                                 cfg            = cfg,
                                 users          = users,
                                 isAdmin        = admin.isAdmin,
                                 today          = today)