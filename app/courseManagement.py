# ADD ANY IMPORTS HERE
from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser
from app.logic import databaseInterface
from app.logic import functions
from app.logic.redirectBack import redirect_url
import pprint

#CROSS LISTED COURSES#


@app.route(
    "/courseManagement/crossListed/",
    defaults={
        'tid': 0},
    methods=[
        "GET",
        "POST"])
@app.route("/courseManagement/crossListed/<tid>", methods=["GET", "POST"])
def crossListed(tid):
    # DATA FOR THE NAVBAR AND SIDE BAR
    terms = Term.select().order_by(-Term.termCode)
    if tid == 0:
        tid = terms[0].termCode

    page = "crossListed"
    authorizedUser = AuthorizedUser()
    ##DATA FOR THE CROSS LISTED COURSE TABLE##
    crossListedCourses = Course.select().where(Course.crossListed == 1).where(
        Course.term == tid).order_by(+Course.schedule).order_by(+Course.rid)

    instructors = databaseInterface.createInstructorDict(crossListedCourses)

    ##DATA FOR THE ADD COURSE FORM##
    courseInfo = BannerCourses.select().order_by(
        BannerCourses.number).order_by(
        BannerCourses.subject)
    users = User.select(User.username, User.firstName, User.lastName)
    schedules = BannerSchedule.select()
    rooms = Rooms.select()
    return render_template("crossListed.html",

                           cfg=cfg,
                           isAdmin=authorizedUser.isAdmin(),
                           allTerms=terms,
                           page=page,
                           currentTerm=int(tid),
                           courses=crossListedCourses,
                           instructors=instructors,
                           courseInfo=courseInfo,
                           users=users,
                           schedules=schedules,
                           rooms=rooms
                           )
#############################
#SCHEDULE AND ROOM CONFLICTS#
#############################


@app.route("/courseManagement/conflicts/<tid>", methods=["GET"])
def conflictsListed(tid):
    #DATA FOR THE NAVEBAR AND SIDEBAR#
    page = "conflicts"
    terms = Term.select().order_by(-Term.termCode)
    authorizedUser = AuthorizedUser()

    # need a something to hold the conflicts
    conflict_dict = dict()

    # we need the dict keys to loop through in the view
    dict_keys = []

    buildings = databaseInterface.getAllBuildings()

    for building in buildings:

        # we want a clean conflicts list for each room
        buildingConflicts = []

        rooms = databaseInterface.getRoomsByBuilding(building)

        for room in rooms:

            # gets all of the courses by room where schedule is none
            # and filters ones special scheduleID ZZZ
            specialScheduleCourseList, courseList = functions.getCoursesByRoom(
                room.rID, tid)

            while len(courseList):
                current_course = courseList.pop()

                # NEEDED TO PREVENT SEG FAULT
                if len(courseList):
                    buildingConflicts += functions.getConflicts(
                        current_course, courseList)

        instructors = {}
        if len(buildingConflicts):

            buildingConflicts = functions.removeDuplicates(buildingConflicts)

            dict_keys.append(building.building)
            # SET THE KEY(building name) TO THE VALUE(list of course objects)
            conflict_dict[building.building] = buildingConflicts
            # DATA FOR THE CONFLICTS TABLE
            instructors = databaseInterface.createInstructorDict(
                buildingConflicts)
    return render_template("conflicts.html",
                           cfg=cfg,
                           isAdmin=authorizedUser.isAdmin(),
                           allTerms=terms,
                           page=page,
                           currentTerm=int(tid),
                           conflicts_dict=conflict_dict,
                           dict_keys=dict_keys,
                           instructors=instructors
                           )
################
#CHANGE TRACKER#
################


@app.route("/courseManagement/tracker/<tid>/", methods=["GET"])
def trackerListed(tid):
    # DATA FOR THE NAVBAR AND SIDE BAR
    page = "tracker"
    terms = Term.select().order_by(-Term.termCode)
    authorizedUser = AuthorizedUser()

    # DATA FOR THE CHANGE TRACKER PAGE
    # ALL OF THIS CAME FROMT HE COURSECHANGE.PY
    if (request.method == "GET"):
        if authorizedUser.isAdmin():

            courses = CourseChange.select().where(CourseChange.verified == False).order_by(CourseChange.term)

            instructorsDict = databaseInterface.createInstructorDict(courses)

            colorClassDict = functions.getColorClassDict(courses)
        '''
      DATA STRUCTURES
      NOTE: The keys for both dictionaries the course identification number
        classDict[cId] = [className,className,className,className,className]
        *Then it will return a list of classnames that can be accessed through an index

        instructorsDict[cid] = intructorCourseChange peewee object
      '''
        return render_template("tracker.html",
                               cfg=cfg,
                               isAdmin=authorizedUser.isAdmin(),
                               allTerms=terms,
                               page=page,
                               currentTerm=int(tid),
                               courses=courses,
                               instructorsDict=instructorsDict,
                               classDict=colorClassDict
                               )
    else:
        return render_template("404.html", cfg=cfg)


@app.route("/courseManagement/tracker/verified", methods=["POST"])
def verifyChange():
    if (request.method == "POST"):
        page = "/" + request.url.split("/")[-1]
        authorizedUser = AuthorizedUser()
        if authorizedUser.isAdmin():
            data = request.form
            verify = DataUpdate()
            verify.verifyCourseChange(data)
            message = "Course Change: {0} has been verified".format(data['id'])
            log.writer("INFO", page, message)
            flash("Your course has been marked verified")
            return redirect(redirect_url())
    
