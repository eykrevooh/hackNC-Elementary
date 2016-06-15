from allImports import *
class DataUpdate():
    
  def __init__(self):
    self.username = authUser(request.environ)
    self.level    = 0
      
  def checkUserLevel(self, prefix):
    admin = User.get(User.username == self.username)
    subject = Subject.get(Subject.prefix == prefix)
    divisionChair = (DivisionChair.select()
                      .where(DivisionChair.username == self.username)
                      .where(DivisionChair.did == subject.pid.division.dID))
    
    
    programChair  = ProgramChair.select().where(ProgramChair.username == self.username).where(ProgramChair.pid == subject.pid.pID)
    
    if admin.isAdmin or divisionChair.exists() or programChair.exists():
      return True
          
  def addCourse(self, data, term, instructors, prefix, schedule):
    if self.checkUserLevel(prefix):
      subject, number, title = data['ctitle'].split(None, 2)
      bannerCourse = BannerCourses.select().where(BannerCourses.subject == subject).where(BannerCourses.number == number)
      bannerCourse = bannerCourse[0]  # grabs the first bannerCourse object with a name matching subject and course number (e.g. CSC 236)

      if int(number) % 100 == 86:
        specialTopicName = data['specialTopicName']
      else:
        specialTopicName = None
      if data['capacity'] == "":
        capacity = None
      else:
        capacity = data['capacity']
      
      course = Course(bannerRef     = bannerCourse.reFID,
                  prefix            = prefix,
                  term              = int(term),
                  schedule          = schedule,
                  capacity          = capacity,
                  specialTopicName  = specialTopicName,
                  notes             = data['requests']
                )
      course.save()
      for professor in instructors:
        instructor = InstructorCourse(username = professor, course = course.cId)
        instructor.save()
    return course.cId
  
  
  def editCourse(self, data, prefix, professors):
    if self.checkUserLevel(prefix):
      course = Course.get(Course.cId == int(data['cid']))
      
      course.term     = data['term']
      course.capacity = data['capacity']
      course.schedule = data['schedule']
      course.notes  = data['notes']
      course.lastEditBy = authUser(request.environ)
      
      course.save()
      
      oldInstructors = InstructorCourse.select().where(InstructorCourse.course == int(data['cid']))
      for oldInstructor in oldInstructors:
        if oldInstructor.username.username not in professors:
          oldInstructor.delete_instance()
        else:
          professors.remove(oldInstructor.username.username)
      
      for professor in professors:
        newInstructor = InstructorCourse(username = professor, course = int(data['cid']))
        newInstructor.save()
  
  def deleteCourse(self, data, prefix):
    if self.checkUserLevel(prefix):
      course = Course.get(Course.cId == int(data['cid']))
      course.delete_instance()
      instructors = InstructorCourse.select().where(InstructorCourse.course == int(data['cid']))
      for instructor in instructors:
        instructor.delete_instance()
  
######################################################################################
  def isTermEditable(self, tid):
    term = Term.get(Term.termCode == int(tid))
    return term.editable
  
  def addCourseChange(self, cid, prefix, changeType):
    if self.checkUserLevel(prefix):
      course = Course.get(Course.cId == cid)
      instructors = InstructorCourse.select().where(InstructorCourse.course == cid)
      newcourse, created = CourseChange.create_or_get( 
                                cId               = course.cId,
                                bannerRef         = course.bannerRef,
                                prefix            = course.prefix,
                                term              = course.term,
                                schedule          = course.schedule,
                                specialTopicName  = course.specialTopicName,
                                capacity          = course.capacity,
                                notes             = course.notes,
                                lastEditBy        = course.lastEditBy,
                                changeType        = changeType
                              )
      newcourse.save()
      for professor in instructors:
        instructor = InstructorCourseChange(username = professor.username, course = professor.course)
        instructor.save()
      
      return created
    
  def editCourseChange(self, cid, prefix, changeType):
    if self.checkUserLevel(prefix):
      newcourse = Course.get(Course.cId == cid)
      course = CourseChange.get(CourseChange.cId == cid)
      
      course.term     = newcourse.term
      course.capacity = newcourse.capacity
      course.schedule = newcourse.schedule
      course.notes = newcourse.notes
      course.lastEditBy = newcourse.lastEditBy
      course.changeType = changeType
    
      course.save()
      
      newInstructors = InstructorCourse.select().where(InstructorCourse.course == cid)
      professors = InstructorCourseChange.select().where(InstructorCourseChange.course == cid)
      
      instructors =[]
      for professor in professors:
        instructors.append(professor)
      
      for newInstructor in newInstructors:
        professor = InstructorCourseChange.select().where(InstructorCourseChange.course == cid).where(InstructorCourseChange.username == newInstructor.username)
        if professor.exists():
          instructors.remove(professor[0])
        else:
          InstructorChange(username = oldInstructor.username, cid = cid).save()
      
      for instructor in instructors:
        instructor.delete_instance()
      
      course.verified=False
      course.save()
  
  def verifyCourseChange(self, data):
    if self.checkUserLevel('CSC'):
      course = CourseChange.get(CourseChange.cId == int(data['id']))
      course.delete_instance()
      instructors = InstructorCourseChange.select().where(InstructorCourseChange.course == int(data['id']))
      for instructor in instructors:
        instructor.delete_instance()