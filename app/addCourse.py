from allImports import *
from updateCourse import DataUpdate
from getAuthUser import AuthorizedUser
from app.logic.databaseInterface import addCourseInstructors
from app.logic.NullCheck import NullCheck


'''
adds the course to the course table and to the course change if needed
'''


@app.route(
    "/addCourse/<tid>/<page>/",
    defaults={
        'prefix': 0},
    methods=["POST"])
@app.route("/addCourse/<tid>/<page>/<prefix>", methods=["POST"])
def addCourses(tid, page, prefix):
    # get the username
    username = authUser(request.environ)

    # check to see if they are authorized to change anything
    authorizedUser = AuthorizedUser(username, prefix)

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
                        notes=data['requests'],
                        crossListed=int(data['crossListed']),
                        rid=values['rid']
                        )

        course.save()

        # we will need to keep the cid to enter the intructors
        cid = course.cId
        addCourseInstructors(instructors, course.cId)

        newCourse = DataUpdate()
        if not newCourse.isTermEditable(tid):  # IF THE TERM IS NOT EDITABLE
            # ADD THE COURSE TO THE COURSECHANGE TABLE
            newCourse.addCourseChange(cid, cfg["changeType"]["create"])

        # log the change
        message = "Course: #{0} has been added".format(cid)
        log.writer("INFO", current_page, message)
        flash("Course has successfully been added!")
        if page == "courses":
            return redirect(url_for("courses", tID=str(tid), prefix=prefix))
        else:
            url = "courseManagement/" + page + "/" + str(tid)
            return redirect(url)
    else:
        return render_template("404.html", cfg=cfg)
