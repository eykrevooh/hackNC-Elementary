from allImports import *
from app.logic.NullCheck import NullCheck
from app.logic import databaseInterface
import pprint


class DataUpdate():

    def __init__(self):
        self.username = authUser(request.environ)
        self.level = 0

    def createColorString(self, changeType):
        ''' Purpose: This method will create a comma seperated list depending on the changeType entered
        @param -changeType {string} = This should only ever be a type located in the config.yaml
        -->Author: CDM 20160713 '''
        # SET THE COLOR SCHEME FOR THE TD'S
        color = cfg["columnColor"][changeType]
        colorList = []
        for x in range(len(cfg["tableLayout"]["order"])):
            colorList.append(color)
            
        tdcolors = ",".join(colorList)

        return tdcolors

    def addCourseChange(self, cid, changeType):

        tdcolors = self.createColorString(changeType)
        # ADD THE PROFESSORS TO INTRUCTORCOURSECHANGE
        course = Course.get(Course.cId == cid)

        instructors = InstructorCourse.select().where(InstructorCourse.course == cid)
        for instructor in instructors:
            addInstructorChange = InstructorCourseChange(
                username=instructor, course=course.cId)
            addInstructorChange.save()
        # ADD THE COURSE TO COURSECHANGE
        # MORE INFO ABOUT THE NULL CHECK CAN BE FOUND
        nullCheck = NullCheck()
        values = nullCheck.add_course_change(course)
        newcourse = CourseChange(
            cId=course.cId,
            # WE DON'T HAVE TO CHECK THIS VALUE BECAUSE IT CAN NEVER BE
            # NULL
            prefix=course.prefix.prefix,
            bannerRef=values['bannerRef'],
            # WE DON'T HAVE TO CHECK THIS VALUE BECAUSE IT CAN NEVER BE
            # NULL
            term=course.term.termCode,
            schedule = values['schedule'],
            specialTopicName=course.specialTopicName,
            capacity=course.capacity,
            
            notes=course.notes,
            lastEditBy=self.username,
            changeType=changeType,
            rid=values['rid'],
            crossListed=int(course.crossListed),
            tdcolors=tdcolors)
        number = newcourse.save(force_insert=True)
        # WHENEVER CERTAINING A NON AUTO INCREMENTED PRIMARY KEY
        # IT IS REQUIRED TO PUT force_insert=True
        return True

    


    def verifyCourseChange(self, data):
        course = CourseChange.get(CourseChange.cId == data['id'])
        course.delete_instance()
        instructors = InstructorCourseChange.select().where(
            InstructorCourseChange.course == int(data['id']))
        for instructor in instructors:
            instructor.delete_instance()
