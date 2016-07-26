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
         users          = User.select()
         program        = Program.get()
         today          = datetime.date.today()
         #WE WANT THE USER TO HAVE THE ABILITY TO SELECT A YEAR AGO AND THREE YEARS PAST THE CURRENT YEAR
         years       = []
         #START WITH ONE YEAR AGO
         year  = int(time.strftime("%Y")) - 1   
         for x in range(5):
            if x == 0:
               #APPEND THE ONE YEAR AGO
               years.append(str(year))          
            year += 1
            #APPEND CURRENT NUMBER PLUS ONE
            years.append(str(year))          
         return render_template("systemManagement.html",
                                 terms          = terms,
                                 years          = years,
                                 program        = program,
                                 cfg            = cfg,
                                 users          = users,
                                 isAdmin        = admin.isAdmin,
                                 today          = today)