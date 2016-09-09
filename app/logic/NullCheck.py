from app.allImports import *


class NullCheck():
  def __init__(self):
    self.username = authUser(request.environ)
    self.level    = 0
  #ADD_COURSE_FORM#
  def add_course_form(self,data):
    '''Purpose:WHENEVER A COURSE IS ADDED WE NEED TO CHECK THE VALUES POSTED BY 
       THE ADD COURSE IF AN EMPTY STRING EXISTS, IF IT DOES WE NEED TO REPLACE IT WITH NONE SO THAT 
       IT CAN BE ENTERED AS NULL IN THE DB
       -----------------------------------
       pre: DATA MUST COME A REQUEST.FORM
       POST: WILL RETURN A DICTIONARY THAT CONTAINS THE PROPER VALUES FOR EACH ELEMENT IN THE FORM. 
       WHICH WILL ALLSO INCLUDE TURNING "" INTO NONE VALUES'''
    value = dict()
    #SPLIT UP THE COURSE TITLE e.g.: CSC 126 robotics into subject = CSC, number = 126, title = robotics
    prefix, number, title = data['ctitle'].split(None, 2)
    value['prefix'] = prefix
    #GRABS THE FIRST BANNERCOURSE OBJECT WITH A NAME MATCHING SUBJECT AND COURSE NUMBER (E.G. CSC 236)
    bannerCourse = BannerCourses.select().where(BannerCourses.subject == prefix).where(BannerCourses.number == number)
    bannerCourse = bannerCourse[0] 
    value['bannerRef']=bannerCourse.reFID
    #THE SPECIAL TOPICS FELD
    if len(str(number).split('86')) > 1:
       value['specialTopicName'] = data['specialTopicName']
    else:
       value['specialTopicName'] = None
    #CHECK DATA FOR EMPTY STRING
    #THESE ARE ALL OF THE VALUES THAT COULD CONTAIN AN EMPTY STRING
    checkList = ['capacity','schedule','rid','requests'] 
    for item in checkList:
      if data[item]=="":
        value[item]=None
      else:
        value[item]=data[item]
    '''CURRENT DICTIONARY KEYS:['subject','bannerRef','specialTopicName','capacity','schedule','rid']'''
    return value
  #_ADD_COURSE_CHANGE#
  def add_course_change(self,course):
    '''PURPOSE: 
    WHENEVER A COURSE IS ADDED TO THE COURSECHANGES TABLE, 
    SOME FIELDS REQUIRE DATA TO BE ACCESSED THROUGH FOREIGN KEY RELATIONSHIPS.
    HOWEVER THIS DATA CAN ALSO BE NULL, WHICH CAUSES THE PAGE TO BREAK BECAUSE WE ARE TRYING
    TO ACCESS ATTRIBUTES OF A FOREIGN KEY FIELD OF A NONE VALUE. ERROR-->AttributeError: 'NoneType' object has no attribute
       FOR EXAMPLE:
     -bannerRef =  course.bannerRef.reFID --> course.NONE.reFID
    IN ORDER TO PREVENT THIS ERROR WE SHOULD ONLY TRY TO ACCESS THE FOREIGN KEY FIELDS IF THE VALUE IS NOT NONE
       PRE: 
    -COURSE NEEDS TO BE A PEEWEE COURSE OBJECT
       POST:
    -WE WILL PASS BACK A DICTIONARY WITH THE PROPER VALUES MATCHING THE KEY
    '''
    value = dict()
    '''VALUES BEING CHECKED = [course.bannerRef, course.schedule, course.rid]'''
    if course.bannerRef == None:
      value['bannerRef'] = None
    else:
      value['bannerRef'] = course.bannerRef.reFID
    if course.schedule == None:
      value['schedule'] = None
    else:
      value['schedule'] = course.schedule.sid
    if course.rid == None:
      value['rid'] = None
    else:
      value['rid'] = course.rid.rID
    return value
    
    
    
