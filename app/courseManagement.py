#ADD ANY IMPORTS HERE
from allImports import *
from updateCourse import DataUpdate

@app.route("/courseManagement/crossListed/", defaults={'tid':0}, methods=["GET", "POST"])
@app.route("/courseManagement/crossListed/<tid>", methods = ["GET"])
def crossListed(tid):
    if tid == 0:
        term = Term.select().get()
        tid = term.termCode
    # do stuff
    page = "crossListed"
    terms = Term.select().order_by(-Term.termCode)
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    ## START WORKING ON THE DATA NEEDED FOR CROSS lISTED##
    crossListedCourses = Course.select().where(Course.crossListed == 1).where(Course.term == tid).order_by(+Course.schedule).order_by(+Course.rid)
    instructors = {}
    for course in crossListedCourses:
        instructors[course.cId] = InstructorCourse.select().where(InstructorCourse.course == course.cId)
    return render_template("crossListed.html",
                            cfg              = cfg,
                            isAdmin          = admin.isAdmin,
                            allTerms         = terms,
                            page             = page,
                            currentTerm      = tid,
                            courses          = crossListedCourses,
                            instructors      = instructors
                          )

@app.route("/courseManagement/conflicts/<tid>", methods = ["GET"])
def conflictsListed(tid):
    # do stuff
    page = "conflicts"
    terms = Term.select().order_by(-Term.termCode)
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    return render_template("conflicts.html",
                            cfg              = cfg,
                            isAdmin          = admin.isAdmin,
                            allTerms      = terms,
                            page = page,
                            currentTerm     = tid
                          )


@app.route("/courseManagement/tracker/<tid>", methods = ["GET"])
def trackerListed(tid):
    # do stuff
    page = "tracker"
    terms = Term.select().order_by(-Term.termCode)
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    return render_template("tracker.html",
                            cfg              = cfg,
                            isAdmin          = admin.isAdmin,
                            allTerms      = terms,
                            page = page,
                            currentTerm     = tid
                          )

