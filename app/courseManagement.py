#ADD ANY IMPORTS HERE
from allImports import *
from updateCourse import DataUpdate

@app.route("/courseManagement/crossListed/", defaults={'sid':0}, methods=["GET", "POST"])
@app.route("/courseManagement/crossListed/<sid>", methods = ["GET"])
def crossListed(sid):
    if sid == 0:
        sid = Term.select(Term.termCode).get()
    # do stuff
     ##DATA NEEDED FOR SIDEBAR##
    page = "crossListed"
    terms = Term.select().order_by(-Term.termCode)
    ##DATA NEEDED FOR SIDEBAR##
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    return render_template("crossListed.html",
                            cfg              = cfg,
                            isAdmin          = admin.isAdmin,
                            allTerms      = terms,
                            page = page,
                            currentTerm     = sid
                          )

@app.route("/courseManagement/conflicts/<sid>", methods = ["GET"])
def conflictsListed(sid):
    # do stuff
     ##DATA NEEDED FOR SIDEBAR##
    page = "conflicts"
    terms = Term.select().order_by(-Term.termCode)
    ##DATA NEEDED FOR SIDEBAR##
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    return render_template("conflicts.html",
                            cfg              = cfg,
                            isAdmin          = admin.isAdmin,
                            allTerms      = terms,
                            page = page,
                            currentTerm     = sid
                          )


@app.route("/courseManagement/tracker/<sid>", methods = ["GET"])
def trackerListed(sid):
    # do stuff
     ##DATA NEEDED FOR SIDEBAR##
    page = "tracker"
    terms = Term.select().order_by(-Term.termCode)
    ##DATA NEEDED FOR SIDEBAR##
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    return render_template("tracker.html",
                            cfg              = cfg,
                            isAdmin          = admin.isAdmin,
                            allTerms      = terms,
                            page = page,
                            currentTerm     = sid
                          )

