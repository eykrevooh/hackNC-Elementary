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
    
    if admin.isAdmin or divisionChair or programChair:
      return True
          
  def addCourse(self, data, term, instructors, prefix):
    if self.checkUserLevel(prefix):
      prefix, number, title = data['ctitle'].split(None, 2)
      bannerCourse = BannerCourses.get(BannerCourses.subject == prefix)
                      
      # course.save()
      course = Course(bannerRef     = bannerCourse.reFID,
                  prefix            = prefix,
                  term              = int(term),
                  schedule          = int(data['schedule']),
                  capacity          = int(data['capacity']),
                  roomPref          = data['requests']
                )
      course.save()
      print course.cId
      for professor in instructors:
        instructor = InstructorCourse(username = professor, course = course.cId)
        instructor.save()
  
  
  def editCourse(self, data, prefix, professors):
    if self.checkUserLevel(prefix):
      course = Course.get(Course.cId == int(data['cid']))
      
      course.term     = data['term']
      course.capacity = data['capacity']
      course.schedule = data['schedule']
      course.roomPref = data['notes']
      
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
      