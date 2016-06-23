#ADD ANY IMPORTS HERE
from allImports import *
from updateCourse import DataUpdate
######################
#CROSS LISTED COURSES#
######################
@app.route("/courseManagement/crossListed/", defaults={'tid':0}, methods=["GET", "POST"])
@app.route("/courseManagement/crossListed/<tid>", methods = ["GET"])
def crossListed(tid):
    #DATA FOR THE NAVBAR AND SIDE BAR
    terms = Term.select().order_by(-Term.termCode)
    if tid == 0:
        counter = 0
        for term in terms:
            if counter == 0:
                tid = term.termCode
            counter += 1
    page = "crossListed"
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    ##DATA FOR THE CROSS LISTED COURSE TABLE##
    crossListedCourses = Course.select().where(Course.crossListed == 1).where(Course.term == tid).order_by(+Course.schedule).order_by(+Course.rid)
    instructors = {}
    for course in crossListedCourses:
        instructors[course.cId] = InstructorCourse.select().where(InstructorCourse.course == course.cId)
    ##DATA FOR THE ADD COURSE FORM##
    courseInfo = BannerCourses.select().order_by(BannerCourses.number).order_by(BannerCourses.subject)
    users   = User.select(User.username, User.firstName, User.lastName)
    schedules = BannerSchedule.select()
    rooms     = Rooms.select()
    return render_template("crossListed.html",
                            cfg              = cfg,
                            isAdmin          = admin.isAdmin,
                            allTerms         = terms,
                            page             = page,
                            currentTerm      = tid,
                            courses          = crossListedCourses,
                            instructors      = instructors,
                            courseInfo       = courseInfo,
                            users            = users,
                            schedules        = schedules,
                            rooms            = rooms
                          )
#############################
#SCHEDULE AND ROOM CONFLICTS#
#############################
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
################
#CHANGE TRACKER#
################
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

