#ADD ANY IMPORTS HERE
from allImports import *
from updateCourse import DataUpdate
conflicts       = load_config(os.path.join(here, 'conflicts.yaml'))
######################
#CROSS LISTED COURSES#
######################
@app.route("/courseManagement/crossListed/", defaults={'tid':0}, methods=["GET", "POST"])
@app.route("/courseManagement/crossListed/<tid>", methods = ["GET","POST"])
def crossListed(tid):
    #DATA FOR THE NAVBAR AND SIDE BAR
    terms = Term.select().order_by(-Term.termCode)
    if tid == 0:
      counter = 0
      for term in terms:
          if counter == 0:
              tid = term.termCode
          counter += 1
    page    = "crossListed"
    username= authUser(request.environ)
    admin   = User.get(User.username == username)
    ##DATA FOR THE CROSS LISTED COURSE TABLE##
    crossListedCourses  = Course.select().where(Course.crossListed == 1).where(Course.term == tid).order_by(+Course.schedule).order_by(+Course.rid)
    instructors         = {}
    for course in crossListedCourses:
        instructors[course.cId] = InstructorCourse.select().where(InstructorCourse.course == course.cId)
    ##DATA FOR THE ADD COURSE FORM##
    courseInfo  = BannerCourses.select().order_by(BannerCourses.number).order_by(BannerCourses.subject)
    users       = User.select(User.username, User.firstName, User.lastName)
    schedules   = BannerSchedule.select()
    rooms       = Rooms.select()
    return render_template("crossListed.html",
                            cfg              = cfg,
                            isAdmin          = admin.isAdmin,
                            allTerms         = terms,
                            page             = page,
                            currentTerm      = int(tid),
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
    #DATA FOR THE NAVEBAR AND SIDEBAR#
    page      = "conflicts"
    terms     = Term.select().order_by(-Term.termCode)
    username  = authUser(request.environ)
    admin     = User.get(User.username == username)
    #DATA FOR THE CONFLICTS PAGE#
    roomConflicts = []      #CREATE AN EMPTY ROOM CONFLICTS LIST
    rooms = Rooms.select()  #SELECT ALL OF THE ROOMS
    for room in rooms:      #LOOP THOUGH ALL OF THE ROOMS
      courseList = []       #CREATE AN EMPTY COURSE LIST
      courseConflicts = []  #CREATE AN EMPTY LIST FOR COURSE OBJECTS TO BE STORED IN
      courses = Course.select().where(room.rID == Course.rid, Course.term == tid) #FIND COURSES IN ROOM FOR THAT TERM
      if courses:           #MAKE SURE THE ROOM CONTAINS COURSES ==> THIS PREVENTS ERRORS ON TRYING TO ACCESS ERRORS THAT DON'T EXSIST
          for course in courses:
              if course.schedule != "ZZZ": #ZZZ IS A CUSTOM TIME SLOT THAT SHOULDN'T BE INCLUDED IN THE COURSE LIST BECAUSE IT'S NOT IN CONFLICTS.YAML
                  courseList.append(course)#APPEND THE WHOLE COURSE OBJECT TO THE LIST
              else:
                  courseConflicts.append(course) 
                  #SINCE ZZZ IS A SPECIAL TIME ENTRY
                  #WE WILL APPEND IT TO THE CONFLICTS LIST SO THAT SHE CAN MANUALLY CHECK IT 
          while courseList != []: 
              current_course = courseList.pop()
              if courseList != []: #CHECK TO SEE IF NOW EMPTY ==> NEEDED TO PREVENT SEG FAULT
                for course in courseList:
                  result = conflicts[current_course.schedule.sid][course.schedule.sid] #ACCESS THE SID THROUGH THE COURSE OBJECT
                  if result == 1:
                    #APPEND BOTH COURSE OBJECTS TO THE CONFLICTS LIST
                    courseConflicts.append(current_course) 
                    courseConflicts.append(course)         
          if courseConflicts != []:
            #REMOVE THE DUPLICATE OBJECTS IN courseConflicts
            seen = set()
            seen_add = seen.add
            courseConflicts = [x for x in courseConflicts if not (x in seen or seen_add(x))]
            roomConflicts.append([room,courseConflicts]) 
            #CREATE THIS DATA STRUCTURE ---> [x1,[y1,y2,y3]]
            #x1 = a peewee object for the room
            #[y1,y2,y3] = A LIST OF UNIQUE COURSE OBJECTS
            #WE PASS THE OBJECTS SO THA THE DATA STRUCTURE CAN EASIABLY LOOPED THROUGH WITH JINJA ON CONFLICTS.YAML
            #MORE INFORMATION CAN BE FOUND ON ISSUE #46
    print roomConflicts
    return render_template("conflicts.html",
                            cfg              = cfg,
                            isAdmin          = admin.isAdmin,
                            allTerms         = terms,
                            page             = page,
                            currentTerm      = int(tid),
                            conflicts        = roomConflicts,
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

