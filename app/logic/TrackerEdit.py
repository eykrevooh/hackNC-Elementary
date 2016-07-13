from app.allImports import *

class TrackerEdit(cid):
  def __init__():
    '''@colorList will contain the order of color names for the tdColors field
       @cid is a course identification number'''
    self.colorList = [cfg['columnColor']['default']]
    self.cid       = cid
     
    
  def format_data(self,data):
    '''Purpose: To format the form post data to ensure that all empty 
    strings are replaced by None values. Also, ensures that all the data
    in dataKeys exist
    @param -data {dict} -Should always come directly from a request.form
    -> Author: CDM 20160713'''
     try:
        formData = {}
        dataKeys = cfg['editForm']['dataKeys']
        for key in dataKeys:
            formData[key] = data[key] if data[key] != '' else None
        return formData
    except Exception as e:
        #TODO: Log Error
        return 'Error'
        
  def check_course_change():
    '''Purpose to check if the cid exist in courseChange.
    @param  -cid {number} : Course Identification Number
    @return -courseChangeExist: if course exist return peewee object of course else return None
    Author -> CDM 20160713'''
    try:
      courseChangeExist = CourseChange.get(CourseChange.cId == self.cid)
      #Set the class variable colorList to the current tdcolors
      self.colorList    = courseChangeExist.tdcolors.split(",")
      return courseChangeExist
    except CourseChange.DoesNotExist:
      return None
  
    
  def add_color(self, color, courseChangeExist, index):
    if color == 'danger':
      if courseChangeExist is None:
          self.colorList.append(color)
      else:
          self.colorList[index] = color
    else:
      if courseChangeExist is None:
          self.colorList.append(color)
    
    def create_instructor_list():
      '''Purpose: To create a list of instructor usernames from InstructorsCourse matching self.cid
        @param -instructors {{PeeWee Object}}
        @return -instrList {{list user's usernames}}
        Author --> CDM 20160713'''
      findCourseInstructors = InstructorCourse.select().where(InstructorCourse.course == self.cid)
      if instructors:
        instrList = []
        for instructor in instructors:
          instrList.append(instructor.username)
      return innstrList
    
    def add_instructors(usernameList):
      ''' Purpose: To remove the old entries found in InstructorCourseChange if
      there are any then add the new instructors
      Author --> CDM 201607'''
      instructorChange = InstructorCourseChange.select().where(InstructorCourseChange.course == self.cid)
      if instructorChange:
        InstructorCourseChange.delete().where(InstructorCourseChange.course == self.cid).execute()
      if usernameList != []:
        for instructor in usernameList:
          addUser = InstructorCourseChange(course=self.cid, username=instructor)
          addUser.save(force_insert=True)
      return True
    
    def check_instructor_change(newInstructors,courseInstructors): 
      '''Purpose: To record the newInstructors to InstructorCourseChange 
      based off if changes exist. Author --> CDM 20160713
      @param  -newInstructors {{list of strings}}
      @param  -courseInstructors {{list of strings}}
      @return -color{{string}} indicates if a change was made or not
      '''
      if len(newInstructors) == len(courseInstructors):
        duplicates = set(newInstructors) & set(courseInstructors)
        if len(duplicates) == len(newInstructors) and len(duplicates) == len(courseInstructors):
          #No changes where made to the Instructors of this course
          color = cfg['columnColor']['default']
        else:
          color = cfg['columnColor']['update']
          self.add_instructors(newInstructors)
      else:
        color = cfg['columnColor']['update']
        self.add_instructors(newInstructors)
          
    def make_edit(self, data, newInstructors, username):
        '''Purpose: Acts as a main controller for editing a course 
           @param -data {{form.request}}
           @param -newInstructors {{list of usernames}}
           @param -username {{string}} : is the user making the edit
           Author -> CDM 20160713'''
        formData           = self.format_data(data)
        courseChangeExist  = self.check_course_change()
        #Check if the instructors have changed for the course
        courseInstructors  = self.create_instructor_list()
        color              = self.check_instructor_change(newInstructors,courseInstructors)
        #Indicate if a change was made or not using colorList
        #index is for editing a the current tdColors
        index = cfg['tableLayout']['Taught By']  
        self.addColor(color,courseChangeExist,index)     
            
           
        
        # COURSE CHANGE DATA#
        # CHECK COURSE INFO
        course = Course.get(Course.cId == formData['cid'])
        courseSchedule = course.schedule.sid if course.schedule is not None else None
        courseRoom = course.rid.rID if course.rid is not None else None
        #SCHEDULE#
        color = cfg['columnColor']['edit'] if formData[
            'schedule'] != courseSchedule else cfg['columnColor']['default']
        colorList = self.addColor(
            color,
            courseChangeExist,
            colorList,
            cfg['tableLayout']['Schedule'])
        #ROOM#
        color = cfg['columnColor']['edit'] if formData[
            'room'] != courseRoom else cfg['columnColor']['default']
        colorList = self.addColor(
            color,
            courseChangeExist,
            colorList,
            cfg['tableLayout']['Room'])
        # CAPACITY
        color = cfg['columnColor']['edit'] if formData[
            'capacity'] != course.capacity else cfg['columnColor']['default']
        colorList = self.addColor(
            color,
            courseChangeExist,
            colorList,
            cfg['tableLayout']['Capacity'])
        # CROSS LISTED
        color = cfg['columnColor']['edit'] if formData[
            'crossListed'] != course.crossListed else cfg['columnColor']['default']
        colorList = self.addColor(
            color,
            courseChangeExist,
            colorList,
            cfg['tableLayout']['Cross Listed'])
        # NOTES
        color = cfg['columnColor']['edit'] if formData[
            'notes'] != course.notes else cfg['columnColor']['default']
        colorList = self.addColor(
            color,
            courseChangeExist,
            colorList,
            cfg['tableLayout']['Notes'])
        # CREATE A COMMA SEPERATED LIST
        tdColors = ",".join(colorList)
        # SET THE CHANGE TYPE
        if courseChangeExist is None:
            changeType = cfg['changeType']['update']
        elif courseChangeExist.changeType == cfg['changeType']['create'] or courseChangeExist.changeType == cfg['changeType']['create/update']:
            changeType = cfg['changeType']['create/update']
        else:
            # TODO: LOG THE ERROR
            return "Error"
        # UPSERT IS ONLY AVAILABLE FOR SQLITE AND MYSQL DATABASES
        editEntry = CourseChange(
          cId=formData['cid'],
          prefix=course.prefix.prefix,
          bannerRef=course.bannerRef,
          term=formData['term'],
          schedule=formData['schedule'],
          capacity=formData['capacity'],
          notes=formData['notes'],
          # USERNAME IS PASSED INTO THE METHOD
          lastEditBy=username,
          changeType=changeType,
          rid=formData['room'],
          crossListed=['crossListed'],
          tdcolors=tdColors)
        result = editEntry.save(force_insert=True)
        
    