from allImports import *
from updateCourse import DataUpdate



@app.route("/courses/<tID>/<prefix>", methods=["GET", "POST"])
def courses(tID, prefix):
  username = authUser(request.environ)
  
  # These are the necessary components of the sidebar. Should we move them somewhere else?
  page      = "courses"
  divisions = Division.select()
  programs = Program.select()
  subjects = Subject.select()
  
  # Checking the permissions of the user.
  # we need the subject to know if someone if a division chair or a program chair
  subject = Subject.get(Subject.prefix == prefix)
  users   = User.select(User.username, User.firstName, User.lastName)
  
  
  #THIS IS SO THAT WE CAN HAVE THE NAME OF THE PROGRAM AS A HEADER ON THE TOP OF EVERY PAGE
  currentProgram = Program.select().where(Program.pID     == subject.pid,
                                          subject.prefix  == prefix).get()
  
  #THIS IS SO THAT WE CAN HAVE THE TERM BEING VIEWED AT TEH TOP OF EVERY PAGE
  curTermName = Term.get(Term.termCode == tID)
  
  # Checking if person is division chair or program chair
  admin = User.get(User.username == username)
  divisionChair = DivisionChair.select().where(DivisionChair.username == username).where(DivisionChair.did == subject.pid.division.dID)
  programChair  = ProgramChair.select().where(ProgramChair.username == username).where(ProgramChair.pid == subject.pid.pID)
  terms = Term.select().order_by(-Term.termCode)


  
      
  # We need these for populating add course
  courseInfo = BannerCourses.select().where(BannerCourses.subject == prefix).order_by(BannerCourses.number)
  
  schedules = BannerSchedule.select()
  
  courses = Course.select().where(Course.prefix == prefix).where(Course.term == tID)
  
  rooms     = Rooms.select()
  
  
 
  instructors = {}
  for course in courses:
    instructors[course.cId] = InstructorCourse.select().where(InstructorCourse.course == course.cId)
  
  if admin.isAdmin or divisionChair.exists() or programChair.exists():
    return render_template("programAdmin.html",
                          cfg             = cfg,
                          courses         = courses,
                          instructors     = instructors,
                          programs        = programs,
                          divisions       = divisions,
                          subjects        = subjects,
                          currentTerm     = int(tID),
                          courseInfo      = courseInfo,
                          users           = users,
                          schedules       = schedules,
                          allTerms        = terms,
                          isAdmin         = admin.isAdmin,
                          isProgramChair  = divisionChair.exists(),
                          isDivisionChair = programChair.exists(),
                          currentProgram  = currentProgram,
                          curTermName     = curTermName,
                          prefix          = prefix,
                          page            = page,
                          rooms            = rooms
                        )
  else:
    return render_template("program.html",
                            cfg           = cfg,
                            courses       = courses,
                            instructors   = instructors,
                            programs      = programs,
                            divisions     = divisions,
                            subjects      = subjects,
                            currentTerm   = int(tID),
                            allTerms      = terms,
                            currentProgram = currentProgram,
                            curTermName   = curTermName,
                            prefix        = prefix
                          )
