from app.allImports import *
conflicts = load_config(os.path.join(here, 'conflicts.yaml'))
# TODO: standarize docstring see https://www.python.org/dev/peps/pep-0257/
'''
checks whether two schedules conflicts
@param {string} sid1 the schedule id of the first course
@param {string} sid2 the schedule id of the second schedule

@returns {boolean}
'''


def doesConflict(sid1, sid2):
    return conflicts[sid1][sid2]


'''
returns all course that do not have schedule of none
separates the schedules that have ZZZ as schedule ID
@param roomID - id of the room we are looking at
@param termID - id of term the course are being held in

@returns {list} - list of all the courses except ZZ
@returns {list} - list of all courses that have Schedule ID ZZZ
'''


def getCoursesByRoom(roomID, termID):
    specialScheduleCourseList = []
    courseList = []

    courses = Course.select().where(~(Course.schedule >> None),
                                    Course.rid == roomID,
                                    Course.term == termID).order_by(Course.rid)
    for course in courses:
        if course.schedule.sid == 'ZZZ':
            specialScheduleCourseList.append(course)
        else:
            courseList.append(course)

    return(specialScheduleCourseList, courseList)


'''
creates a list of conflicts by checking one course against a list of many
@param {list} courseList - list of courses that need to be checked

return {list} list of conflicts
'''


def getConflicts(currentCourse, courseList):
    conflicts = []
    for course in courseList:
        if doesConflict(currentCourse.schedule.sid, course.schedule.sid):
            conflicts.extend((currentCourse, course))
    return conflicts


'''
removes duplicates from a list
@param {list} list to be parsed through

@returns {list} list without duplicates
'''


def removeDuplicates(array):
    seen = set()
    seenAdd = seen.add
    return [x for x in array if not (x in seen or seenAdd(x))]

'''
returns a dicitionary with the courseID as key
and the colorClass list as value
@param courses - course list to get colors from

@return {Dict} dicitionary of colorClassList
'''


def getColorClassDict(courses):
    colorClassDict = {}
    for course in courses:
        tdClass = course.tdcolors
        tdClassList = tdClass.split(",")
        colorClassDict[course.cId] = tdClassList
    return colorClassDict
