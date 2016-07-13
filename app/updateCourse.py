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
##########################################################################

    def addColor(self, color, courseChangeExist, colorList, index):
        if color == 'danger':
            if courseChangeExist is None:
                colorList.append(color)
            else:
                colorList[index] = color
        else:
            if courseChangeExist is None:
                colorList.append(color)
        return colorList

    def addCourseEdit(self, data, professors, username):
        '''data        = THE DATA FROM THE FORM POST
           professors  = A LIST OF INSTRUCTORS'''
        # ENSURE THAT ESSENTIAL DATA EXSIST#
        # ENSURE THAT ALL THE DATA WE NEED HAS BEEN PASSED SUCCESSFULLY

        try:
            formData = {}
            dataKeys = [
                'cid',
                'term',
                'schedule',
                'room',
                'capacity',
                'crossListed',
                'notes']
            for key in dataKeys:
                # REPLACES ALL EMPTY STRINGS WITH NONE
                formData[key] = data[key] if data[key] != '' else None
            print 'FORM DATA'
            print formData
        except Exception as e:
            # TODO: LOG THE ERROR
            return 'Error'
        # CREATE AN VARIABLE THAT WILL ALLOW US TO KNOW IF AN ENTRY FOR COURSE CHANGE ALREADY EXIST
        # WE NEED TO PUT THIS IN A TRY CATCH BECAUSE IT WILL THROW A
        # DoesNotExist ERROR OTHERWISE
        try:
            courseChangeExist = CourseChange.get(
                CourseChange.cId == formData['cid'])
            # IF THE COURSE CHANGE EXSIST WE WANT TO UPDATE THE CURRENT TDCOLOR
            courseColors = courseChangeExist.tdcolors
            print "courseColors"
            print courseColors
            colorList = courseColors.split(",")
        except CourseChange.DoesNotExist:
            colorList = []
            courseChangeExist = None
        #INSTRUCTOR CHANGE DATA#
        oldInstructors = InstructorCourse.select().where(
            InstructorCourse.course == formData['cid'])
        instructorChange = InstructorCourseChange.select().where(
            InstructorCourseChange.course == formData['cid'])
        if oldInstructors:
            oldList = []
            for instructor in oldInstructors:
                oldList.append(instructor.username)
            matchingUsers = set(professors) & set(oldList)
            # THIS WILL GATHER DUPLICATES NO MATTER THE ORDER
            # e.g.  = [myersco,heggens]=[myersco,heggens] & [heggens,myersco]
            # THEN WE CAN CHECK THE LENGTH OF THE TWO LIST TO SEE IF THERE ARE
            # ANY DIFFERENCES
            if len(matchingUsers) != len(oldList) or len(
                    matchingUsers) != len(professors):
                if instructorChange:
                    InstructorCourseChange.delete().where(
                        InstructorCourseChange.course == formData['cid']).execute()
                for instr in professors:
                    newInstructor = InstructorCourseChange(
                        course=formData['cid'], username=instr)
                    newInstructor.save(force_insert=True)
                color = 'danger'
            else:
                color = 'none'
            # THE INDEXES OF THE POISITION PLACEMENT
            # OF EACH COLUMN IS LOCATED IN THE CONFIG.YAML
            index = cfg['tableLayout']['Taught By']
            colorList = self.addColor(
                color, courseChangeExist, colorList, index)
        else:
            if instructorChange:
                InstructorCourseChange.delete().where(
                    InstructorCourseChange.cId == cId).execute()
            if professors != []:
                for instr in professors:
                    newInstructor = InstructorCourseChange(
                        cId=cId, username=instr)
                    newInstructor.save()
        # COURSE CHANGE DATA#
        # CHECK COURSE INFO
        course = Course.get(Course.cId == formData['cid'])
        courseSchedule = course.schedule.sid if course.schedule is not None else None
        courseRoom = course.rid.rID if course.rid is not None else None
        #SCHEDULE#
        color = cfg['columnColors']['change'] if formData[
            'schedule'] != courseSchedule else cfg['columnColors']['default']
        colorList = self.addColor(
            color,
            courseChangeExist,
            colorList,
            cfg['tableLayout']['Schedule'])
        #ROOM#
        color = cfg['columnColors']['change'] if formData[
            'room'] != courseRoom else cfg['columnColors']['default']
        colorList = self.addColor(
            color,
            courseChangeExist,
            colorList,
            cfg['tableLayout']['Room'])
        # CAPACITY
        color = cfg['columnColors']['change'] if formData[
            'capacity'] != course.capacity else cfg['columnColors']['default']
        colorList = self.addColor(
            color,
            courseChangeExist,
            colorList,
            cfg['tableLayout']['Capacity'])
        # CROSS LISTED
        color = cfg['columnColors']['change'] if formData[
            'crossListed'] != course.crossListed else cfg['columnColors']['default']
        colorList = self.addColor(
            color,
            courseChangeExist,
            colorList,
            cfg['tableLayout']['Cross Listed'])
        # NOTES
        color = cfg['columnColors']['change'] if formData[
            'notes'] != course.notes else cfg['columnColors']['default']
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
        result = editEntry.upsert(force_insert=True)
##########################################################################

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

    def editCourseChange(self, cid, prefix, changeType):
        if self.checkUserLevel(prefix):
            newcourse = Course.get(Course.cId == cid)
            course = CourseChange.get(CourseChange.cId == cid)
            course.term = newcourse.term
            course.capacity = newcourse.capacity
            course.schedule = newcourse.schedule
            course.notes = newcourse.notes
            course.lastEditBy = newcourse.lastEditBy
            course.changeType = changeType
            course.save()
            newInstructors = InstructorCourse.select().where(InstructorCourse.course == cid)
            professors = InstructorCourseChange.select().where(
                InstructorCourseChange.course == cid)
            instructors = []
            for professor in professors:
                instructors.append(professor)
            for newInstructor in newInstructors:
                professor = InstructorCourseChange.select().where(
                    InstructorCourseChange.course == cid).where(
                    InstructorCourseChange.username == newInstructor.username)
                if professor.exists():
                    instructors.remove(professor[0])
                else:
                    InstructorChange(
                        username=oldInstructor.username, cid=cid).save()
            for instructor in instructors:
                instructor.delete_instance()
            course.verified = False
            course.save()

    def verifyCourseChange(self, data):
        if self.checkUserLevel('CSC'):  # WHY IN THE WORLD IS THIS HARD CODED
            course = CourseChange.get(CourseChange.cId == int(data['id']))
            course.delete_instance()
            instructors = InstructorCourseChange.select().where(
                InstructorCourseChange.course == int(data['id']))
            for instructor in instructors:
                instructor.delete_instance()
