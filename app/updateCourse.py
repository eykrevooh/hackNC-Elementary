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

  def addCourseEdit(self, data, professors):
    '''data        = THE DATA FROM THE FORM POST
       professors  = A LIST OF INSTRUCTORS
       KEYS IN DATA
       [cid,room,schedule,term,capacity,notes,crossListed]
       CHANGE TRACKER COLOR ORDER
       [Course Name, Taught By, Schedule, Room, Capacity, Cross Listed, Notes]
    '''
    try: #ENSURE THAT ALL THE DATA WE NEED HAS BEEN PASSED SUCCESSFULLY
      cId         = data['cid']
      schedule    = data['schedule'] if data['schedule'] != '' else None
      room        = data['room'] if data['room'] != '' else None
      capacity    = data['capacity'] if data['capacity'] != '' else None
      crossListed = data['crossListed']
      notes       = data['notes'] if data['notes'] != '' else None
      oldCourse = Course.get().where(Course.cId==cId)
    except Exception as e:
      #TODO: LOG THE ERROR
      return 'Error'
    checkCourse = CourseChange.get(CourseChange.cId==cId )
    # CHECK TO SEE IF THE CID IS IN THE COURSE CHANGE TABLE
    # IF COURSE ALREADY EXSIST IN TABLE
    if checkCourse:
      tdColors = '' #SET A DEFAULT TD COLOR
      ####################
      #INSTRUCTOR CHANGE?#
      ####################
      #TODO: CHECK TO SEE WHAT HAPPENS WHEN EDIT FORM SUBMITS AN EMPTY LIST
      matchingUsernames = []
      oldList = []
      oldInstructors = InstructorCourse.select().where(course)
      for instructor in oldInstructors:
        oldList.append(instructor.username)
      matchingProfs = set(professors) & set(oldList)
      '''
      I DO THIS TO PULL DUPLICATES FROM LIST NO MATTER THE ORDER THE LIST IS IN
      E.G. [myersco,heggens]=[myersco,heggens] & [heggens,myersco]
      NOW WE CAN COMPARE THE LENGTH OF THE MATCHING PROFESSORS WITH BOTH LIST TO SEE IF THEY ARE THE SAME
      '''
      if len(matchingsProfs) != len(oldList) or len(matchingProfs) != len(professors):
        #DELETE THE OLD ELEMENTS FROM INSTRUCTORCOURSECHANGE
        InstructorCourseChange.delete().where(InstructorCourseChange.cId==cId ).execute()
        for instr in professors:
          newInstructor = InstructorCourseChange(cId = cId, username = instr)
          newInstructor.save()
        tdColors.append('danger,') #APPEND THE CLASS NAME DANGER TO INDICATE THE FIELD AS CHANGED
      else:
        tdColors.append('none,')   #APPEND NONE TO INDICATE THAT THE FIELD HASN'T CHANGED
      #START CHECKING ALL OF THE FIELDS FOR DIFFERENCES FROM THE OLD COURSE
      #WE ALSO NEED TO CHECK TO SEE IF COURSE ALREADY EXSISTS
      try:
        currentChange = CourseChange.get().where(CourseChange.cId == cId)
        #WE NEED TO PUT THIS IN A TRY CATCH BECAUSE IT WILL RAISE A DoesNotExist ERROR OTHERWISE
      except CourseChange.DoesNotExist:
        currentChange = None 
      ################  
      #CHECK SCHEDULE#
      ################
      scheduleCheck = None
      if oldCourse.schedule != None:
        scheduleCheck == oldCourse.schedule.sid
      if schedule != 
      
      
        
      
    
  
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