from allImports import *
from app.logic.NullCheck import NullCheck 
class DataUpdate():
  def __init__(self):
    self.username = authUser(request.environ)
    self.level    = 0
      
  def checkUserLevel(self, prefix):
    admin = User.get(User.username == self.username)
    if admin.isAdmin != True:
      subject = Subject.get(Subject.prefix == prefix)
      divisionChair = (DivisionChair.select()
                        .where(DivisionChair.username == self.username)
                        .where(DivisionChair.did      == subject.pid.division.dID))
      programChair  = ProgramChair.select().where(ProgramChair.username == self.username).where(ProgramChair.pid == subject.pid.pID)
    if admin.isAdmin or divisionChair.exists() or programChair.exists():
      return True
    return False
          
  def isTermEditable(self, tid):
    term = Term.get(Term.termCode == int(tid))
    return term.editable
  
  
  def editCourse(self, data, prefix, professors):
    '''This function edits the course in the databse'''
    
    # check to see if the user has privileges to edit
    if self.checkUserLevel(prefix):
       # get the course object
       
      course = Course.get(Course.cId == int(data['cid']))
      course.term       = data['term']
      if data['capacity']:
        course.capacity = data['capacity']
      course.schedule   = data['schedule']
      course.notes      = data['notes']
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
  
      
######################################################################################

  def addCourseEdit(self,cid, data):
    ''' cid  = COURSE ID
        data = THE DATA FROM THE FORM POST '''
    # CHECK TO SEE IF THE CID IS IN THE COURSE CHANGE TABLE
    checkCourse = CourseChange.select().where(CourseChange.cId==cid)
    
  
  def addCourseChange(self, cid, changeType):
    #SET THE COLOR SCHEME FOR THE TD'S
    tdcolors    = 'none,none,none,none,none' #SET A DEFAULT COLOR SCHEME
    if changeType == cfg["changeType"]["create"]:
      tdcolors = 'success,success,success,success,success'
    elif changeType == cfg['changeType']["delete"]:
      tdcolors = 'danger,danger,danger,danger,danger'
    #ADD THE PROFESSORS TO INTRUCTORCOURSECHANGE
    course      = Course.get(Course.cId == cid)
    if self.checkUserLevel(course.prefix):
      instructors = InstructorCourse.select().where(InstructorCourse.course == cid)
      for instructor in instructors:
        addInstructorChange = InstructorCourseChange(username = instructor  , course = course.cId)
        addInstructorChange.save()
      #ADD THE COURSE TO COURSECHANGE
      #MORE INFO ABOUT THE NULL CHECK CAN BE FOUND
      nullCheck = NullCheck()
      values = nullCheck.add_course_change(course)
      newcourse = CourseChange( 
                              cId               = course.cId,
                              prefix            = course.prefix.prefix, #WE DON'T HAVE TO CHECK THIS VALUE BECAUSE IT CAN NEVER BE NULL
                              bannerRef         = values['bannerRef'],
                              term              = course.term.termCode, #WE DON'T HAVE TO CHECK THIS VALUE BECAUSE IT CAN NEVER BE NULL
                              schedule          = values['schedule'],
                              specialTopicName  = course.specialTopicName,
                              capacity          = course.capacity,
                              notes             = course.notes,
                              lastEditBy        = course.lastEditBy,
                              changeType        = changeType,
                              rid               = values['rid'],
                              crossListed       = course.crossListed,
                              tdcolors          = tdcolors
                            )
      number = newcourse.save(force_insert=True)
      #WHENEVER YOU ENTER IN YOUR OWN PRIMARY KEY YOU NEED TO DO FORCE INSER = TRUE ON THE SAVE
      return True
    else:
      print 'DONT HAVE ACCESS'
      return False
  def editCourseChange(self, cid, prefix, changeType):
    if self.checkUserLevel(prefix):
      newcourse         = Course.get(Course.cId == cid)
      course            = CourseChange.get(CourseChange.cId == cid)
      course.term       = newcourse.term
      course.capacity   = newcourse.capacity
      course.schedule   = newcourse.schedule
      course.notes      = newcourse.notes
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
    if self.checkUserLevel('CSC'):    #WHY IN THE WORLD IS THIS HARD CODED
      course = CourseChange.get(CourseChange.cId == int(data['id']))
      course.delete_instance()
      instructors = InstructorCourseChange.select().where(InstructorCourseChange.course == int(data['id']))
      for instructor in instructors:
        instructor.delete_instance()