from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser
from app.logic.databaseInterface import getSidebarElements, createInstructorDict
from app.logic import functions
@app.route("/courses/",defaults={'tID': None,'prefix': None}, methods=["GET", "POST"] )
@app.route("/courses/<tID>/<prefix>", methods=["GET", "POST"])
def courses(tID, prefix):
    page = "courses"
    authorizedUser = AuthorizedUser(prefix)
    username       = authorizedUser.getUsername()
    data = None
    if request.method == "POST":
      data = request.form
    tID, prefix = functions.checkRoute(tID,prefix,username,data)
    

    # Checking the permissions of the user.
    # we need the subject to know if someone if a division chair or a program
    # chair
    authorizedUser = AuthorizedUser(prefix)

    # These are the necessary components of the sidebar. Should we move them
    # somewhere else?

    divisions, programs, subjects = getSidebarElements()
    subject = Subject.get(Subject.prefix == prefix)

    users = User.select(User.username, User.firstName, User.lastName)

    # THIS IS SO THAT WE CAN HAVE THE NAME OF THE PROGRAM AS A HEADER ON THE
    # TOP OF EVERY PAGE
    currentProgram = subject.pid

    # THIS IS SO THAT WE CAN HAVE THE TERM BEING VIEWED AT TEH TOP OF EVERY
    # PAGE
    curTermName = Term.get(Term.termCode == tID)

    terms = Term.select().order_by(-Term.termCode)

    # We need these for populating add course
    courseInfo = BannerCourses.select().where(
        BannerCourses.subject == prefix).order_by(
        BannerCourses.number)

    schedules = BannerSchedule.select().order_by(BannerSchedule.order)

    courses = Course.select().where(
        Course.prefix == prefix).where(
        Course.term == tID)

    rooms = Rooms.select().order_by(Rooms.building)

    instructors = createInstructorDict(courses)
    
    return render_template(
            "course.html",
            cfg=cfg,
            courses=courses,
            instructors=instructors,
            programs=programs,
            divisions=divisions,
            subjects=subjects,
            currentTerm=int(tID),
            courseInfo=courseInfo,
            users=users,
            schedules=schedules,
            allTerms=terms,
            isAdmin=authorizedUser.isAdmin(),
            isProgramChair=authorizedUser.isProgramChair(),
            isDivisionChair=authorizedUser.isDivisionChair(),
            currentProgram=currentProgram,
            curTermName=curTermName,
            prefix=prefix,
            page=page,
            rooms=rooms)