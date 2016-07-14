from allImports import *
from app.logic.NullCheck import NullCheck
import pprint


class DataUpdate():

    def __init__(self):
        self.username = authUser(request.environ)
        self.level = 0

    def checkUserLevel(self, prefix):
        admin = User.get(User.username == self.username)
        if not admin.isAdmin:
            subject = Subject.get(Subject.prefix == prefix)
            divisionChair = (
                DivisionChair.select() .where(
                    DivisionChair.username == self.username) .where(
                    DivisionChair.did == subject.pid.division.dID))
            programChair = ProgramChair.select().where(
                ProgramChair.username == self.username).where(
                ProgramChair.pid == subject.pid.pID)
        if admin.isAdmin or divisionChair.exists() or programChair.exists():
            return True
        return False

    def isTermEditable(self, tid):
        term = Term.get(Term.termCode == int(tid))
        return term.editable

    def editCourse(self, data, prefix, professors):
        '''THIS FUNCTION EDITS THE COURSE DATA TABLE'''
        # check to see if the user has privileges to edit
        if self.checkUserLevel(prefix):
           # get the course object
            course = Course.get(Course.cId == int(data['cid']))
            course.term = data['term']
            if data['capacity']:
                course.capacity = data['capacity']
            course.schedule = data['schedule']
            course.notes = data['notes']
            course.lastEditBy = authUser(request.environ)
            course.save()
            oldInstructors = InstructorCourse.select().where(
                InstructorCourse.course == int(data['cid']))
            for oldInstructor in oldInstructors:
                if oldInstructor.username.username not in professors:
                    oldInstructor.delete_instance()
                else:
                    professors.remove(oldInstructor.username.username)
            for professor in professors:
                newInstructor = InstructorCourse(
                    username=professor, course=int(data['cid']))
                newInstructor.save()

############################################################################################
    def createColorString(self, changeType):
        ''' Purpose: This method will create a comma seperated list depending on the changeType entered
        @param -changeType {string} = This should only ever be a type located in the config.yaml
        -->Author: CDM 20160713 '''
        # SET THE COLOR SCHEME FOR THE TD'S
        color = cfg["columnColor"]["create"] if cfg["changeType"][
            "create"] == changeType else cfg["columnColor"]["delete"]
        colorList = []

        for x in cfg["tableLayout"]["order"]:
            colorList.append(color)
        tdcolors = ",".join(colorList)

        return tdcolors

    def addCourseChange(self, cid, changeType):

        tdcolors = self.createColorString(changeType)
        # ADD THE PROFESSORS TO INTRUCTORCOURSECHANGE
        course = Course.get(Course.cId == cid)

        if self.checkUserLevel(course.prefix):
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
                schedule=values['schedule'],
                specialTopicName=course.specialTopicName,
                capacity=course.capacity,
                notes=course.notes,
                lastEditBy=course.lastEditBy,
                changeType=changeType,
                rid=values['rid'],
                crossListed=course.crossListed,
                tdcolors=tdcolors)
            number = newcourse.save(force_insert=True)
            # WHENEVER CERTAINING A NON AUTO INCREMENTED PRIMARY KEY
            # IT IS REQUIRED TO PUT force_insert=True
            return True
        else:
            print 'DONT HAVE ACCESS'
            return "Error"
#######################################################################################
    def verifyCourseChange(self, data):
        if self.checkUserLevel('CSC'):  # WHY IN THE WORLD IS THIS HARD CODED
            course = CourseChange.get(CourseChange.cId == int(data['id']))
            course.delete_instance()
            instructors = InstructorCourseChange.select().where(
                InstructorCourseChange.course == int(data['id']))
            for instructor in instructors:
                instructor.delete_instance()
