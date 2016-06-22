#ADD ANY IMPORTS HERE
from allImports import *
from updateCourse import DataUpdate

#GRAB THE URL HERE
@app.route("/courseManagement", methods=["GET", "POST"])
def courseManagement():
    ##DATA NEEDED FOR SIDEBAR##
    terms = Term.select().order_by(-Term.termCode)
    ##DATA NEEDED FOR SIDEBAR##
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    return render_template("courseManagement.html",
                            cfg              = cfg,
                            isAdmin          = admin.isAdmin,
                            allTerms      = terms
                          )