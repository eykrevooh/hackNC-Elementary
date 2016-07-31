from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser
from app.logic import databaseInterface
from app.logic.redirectBack import redirect_url


@app.route("/deletecourse/<tid>/<prefix>", methods=["POST"])
def deletecourse(prefix, tid):

    current_page = "/" + request.url.split("/")[-1]

    authorizedUser = AuthorizedUser(prefix)

    # DATA NEEDED FOR MANIPULATION
    # TODO: Change the colors when a course is updated
    dataUpdateObj = DataUpdate()
    data = request.form
    cid = int(data['cid'])
    # START PROCESSING THE DELETION OF THE COURSE
    course = Course.get(Course.cId == cid)
    # MAKE SURE THE USER HAS THE CORRECT RIGHTS TO DELETE A COURSE
    if authorizedUser.isAuthorized():
        if not databaseInterface.isTermEditable(tid):

            change = CourseChange.select().where(CourseChange.cId == cid)
            # IF THE RECORD ALREADY EXSISTED THEN WE NEED TO UPDATE THE
            # INFORMATION
            if change.exists():
                updateRecord = CourseChange.get(CourseChange.cId == cid)
                if updateRecord.changeType == 'create' and not updateRecord.verified:
                    updateRecord.delete_instance()
                else:
                    updateRecord.changeType = cfg["changeType"]["delete"]
                    colors = dataUpdateObj.createColorString(cfg["changeType"]["delete"])
                    updateRecord.tdcolors = colors
                    updateRecord.save()
            else:
                dataUpdateObj.addCourseChange(
                    course.cId, cfg["changeType"]['delete'])
        instructors = InstructorCourseChange.select().where(
            InstructorCourseChange.course == cid)
        for instructor in instructors:
            instructor.delete_instance()
        message = "Course: course {} has been deleted".format(course.cId)
        course.delete_instance()
        
        log.writer("INFO", current_page, message)

    flash("Course has been successfully deleted")
    return redirect(redirect_url())
