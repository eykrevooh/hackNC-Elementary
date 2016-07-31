from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser
from app.logic import databaseInterface
from app.logic.NullCheck import NullCheck
from app.logic.redirectBack import redirect_url


'''
adds the course to the course table and to the course change if needed
'''


@app.route(
    "/addCourse/<tid>/",
    defaults={
        'prefix': 0},
    methods=["POST"])
@app.route("/addCourse/<tid>/<prefix>", methods=["POST"])
def addCourses(tid, prefix):
    # check to see if they are authorized to change anything
    authorizedUser = AuthorizedUser(prefix)

    # only do the bottom if authorized
    if authorizedUser.isAuthorized():
        # set the current page
        current_page = "/" + request.url.split("/")[-1]

        # get the data
        data = request.form

        # instructors need to be a list
        instructors = request.form.getlist('professors[]')

        # start a null checker
        nullCheck = NullCheck()

        values = nullCheck.add_course_form(data)

        # update the course
        course = Course(bannerRef=values['bannerRef'],
                        prefix=values['prefix'],
                        term=int(tid),
                        schedule=values['schedule'],
                        capacity=values['capacity'],
                        specialTopicName=values['specialTopicName'],
                        notes=values['requests'],
                        crossListed=int(data['crossListed']),
                        rid=values['rid']
                        )

        course.save()

        # we will need to keep the cid to enter the intructors
        cid = course.cId
        databaseInterface.addCourseInstructors(instructors, course.cId)

        newCourse = DataUpdate()
        if not databaseInterface.isTermEditable(tid):  # IF THE TERM IS NOT EDITABLE
            # ADD THE COURSE TO THE COURSECHANGE TABLE
            newCourse.addCourseChange(cid, cfg["changeType"]["create"])

        # log the change
        message = "Course: #{0} has been added".format(cid)
        log.writer("INFO", current_page, message)
        flash("Course has successfully been added!")
        return redirect(redirect_url())
    else:
        abort(404) 
