from allImports import *
from updateCourse import DataUpdate


@app.route("/addCourse/<tid>/<page>/", defaults={'prefix':0}, methods=["POST"])
@app.route("/addCourse/<tid>/<page>/<prefix>",methods=["POST"])
def addCourses(tid,page,prefix):
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if prefix != 0:
        subject = Subject.get(Subject.prefix == prefix)
        divisionChair = DivisionChair.select().where(DivisionChair.username == username).where(DivisionChair.did == subject.pid.division.dID)
        programChair  = ProgramChair.select().where(ProgramChair.username == username).where(ProgramChair.pid == subject.pid.pID)
    if admin.isAdmin or divisionChair.exists() or programChair.exists():
      current_page    = "/" + request.url.split("/")[-1]
      data            = request.form
      instructors     = request.form.getlist('professors[]')
      newCourse       = DataUpdate()
      #SPLIT UP THE COURSE TITLE e.g.: CSC 126 robotics into subject = CSC, number = 126, title = robotics
      subject, number, title = data['ctitle'].split(None, 2)
      bannerCourse = BannerCourses.select().where(BannerCourses.subject == subject).where(BannerCourses.number == number)
      bannerCourse = bannerCourse[0]  # grabs the first bannerCourse object with a name matching subject and course number (e.g. CSC 236)
      if int(number) % 100 == 86:
        specialTopicName = data['specialTopicName']
      else:
        specialTopicName = None
      #CHECK CAPACITY
      if data['capacity'] == "":
        capacity = None
      else:
        capacity = data['capacity']
      #CHECK SCHEDULE
      if data["schedule"] == "":
        schedule = None
      else:
        schedule = data["schedule"]
      if data["room"] == "":
        room = None
      else:
        room = data["room"]
      course = Course(bannerRef     = bannerCourse.reFID,
                  prefix            = subject,
                  term              = int(tid),
                  schedule          = schedule,
                  capacity          = capacity,
                  specialTopicName  = specialTopicName,
                  notes             = data['requests'],
                  crossListed       = int(data['crossListed']),
                  rid               = room
                )
      course.save()
      cid = course.cId
      for professor in instructors:
        instructor = InstructorCourse(username = professor, course = course.cId)
        instructor.save()
        if not newCourse.isTermEditable(tid): #IF THE TERM IS NOT EDITABLE WE WANT TO ADD THE INSTRUCTORS TO THE OTHER TABLE
          instructorHistory = InstructorCourseChange(username = professor, course = course.cId)
          instructorHistory.save()
      if not newCourse.isTermEditable(tid):                   # IF THE TERM IS NOT EDITABLE
         newCourse.addCourseChange(cid, "create")     # ADD THE COURSE TO THE COURSECHANGE TABLE
      message = "Course: #{0} has been added".format(cid)
      log.writer("INFO", current_page, message)
      flash("Course has successfully been added!")
      if page == "courses":
        return redirect(url_for("courses", tID = str(tid), prefix = prefix))
      else:
          url = "courseManagement/" + page + "/" + str(tid)
          return redirect(url)
    else:
      return render_template("404.html", cfg=cfg)
    