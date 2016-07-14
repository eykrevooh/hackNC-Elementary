from app.allImports import *
# TODO: standarize docstring see https://www.python.org/dev/peps/pep-0257/


'''
adds the professors from a list to a database
@param {list} professors - list of professors to be added
@param {int} cid = the course id the where the instructors need to be added to
'''


def addCourseInstructors(instructors, cid):
    for instructor in instructors:
        InstructorCourse(username=instructor, course=cid).save()

'''
adds division chair to database
@param {list} users - list of users that need to be added as division chair
@param {int} did - the division id where the division chairs are added to
'''


def addDivisionChairs(users, did):
    for user in users:
        DivisionChair(username=user, did=did).save()

'''
adds division chair to database
@param {list} users - list of users that need to be added as program chair
@param {int} pid - the program id where the program chairs are added to
'''


def addProgramChairs(users, pid):
    for user in users:
        ProgramChair(username=user, pid=pid).save()

'''
creates division
@param {string} name
'''


def createDivision(name):
    division = Division(name=name)
    division.save()
    return(division.name, division.dID)

'''creates program
@param {string} name
@param {int} divisionID

@returns string, int
'''


def createProgram(name, divisionID):
    program = Program(name=name, division=divisionID)
    program.save()
    return(program.name, program.pID)


'''
gets elements for the course sidebar
@returns selectQuery
'''


def getSidebarElements():
    return (Division.select(), Program.select(), Subject.select())



''' gets the instructors belonging to a course
@param {list} courses - list of courses

@returns{dict} dictionary of courses keys and instructor values
'''


def createInstructorDict(courses):
    instructors = {}
    for course in courses:
        instructors[course.cId] = InstructorCourse.select().where(
            InstructorCourse.course == course.cId)
    return instructors

'''
gets all of the buildings
@returns query object of the buildings
'''


def getAllBuildings():
    return Rooms.select(Rooms.building).distinct()

'''
gets all the rooms that belong to a building
'''


def getRoomsByBuilding(building):
    return Rooms.select().where(Rooms.building == building.building)

'''
gets all terms
return terms
'''


def getAllTerms():
    return Term.select().order_by(-Term.termCode)
    
    
def isTermEditable(termID):
    ''' returns booleans stating whether the term is editable'''
    return Term.get(Term.termCode == int(termID)).editable
    

def editInstructors(newInstructors, courseID):
    ''' edits the instructs give a list of the new instructors
        @param {list} newInstructors - list of new instructors
        @param {int} courseID
    '''
    oldInstructors = InstructorCourse.select().where(
            InstructorCourse.course == courseID)
    for oldInstructor in oldInstructors:
            if oldInstructor.username.username not in newInstructors:
                oldInstructor.delete_instance()
            else:
                newInstructors.remove(oldInstructor.username.username)
    for instructor in newInstructors:
            newInstructor = InstructorCourse(
                username=instructor, course=courseID)
            newInstructor.save()
            
            
def editCourse(data, prefix, professors):
        '''THIS FUNCTION EDITS THE COURSE DATA TABLE'''
        # check to see if the user has privileges to edit
        # get the course object
        course = Course.get(Course.cId == int(data['cid']))
        course.rid = data['room']
        course.term = data['term']
        if data['capacity']:
            course.capacity = data['capacity']
        schedule = data['schedule'] if data['schedule'] else None
        course.schedule = schedule
        notes = data['notes'] if data['notes'] else None
        course.notes = notes
        course.lastEditBy = authUser(request.environ)
        course.save()
        editInstructors(professors, data['cid'])    
    
def isTermEditable(termID):
    ''' returns booleans stating whether the term is editable'''
    return Term.get(Term.termCode == int(termID)).editable