from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser
import datetime


@app.route("/", methods=["GET", "POST"])
def deadlineDisplay():
    if (request.method == "GET"):
        authorizedUser = AuthorizedUser()
        checkIfUser    = authorizedUser.checkIfUser()
        isAdmin = authorizedUser.isAdmin()
        today = datetime.date.today()
        dates=Deadline.select().where(Deadline.date > today).distinct().order_by(
            Deadline.date)
        
    return render_template("deadline.html",
                           cfg=cfg,
                           isAdmin=isAdmin,
                           deadlines=dates,
                           today=today)
