from allImports import *

@app.route("/readCourses", methods = ["GET"])

def readCourses():
    """This function will get data about courses from database """
    courses = Courses.select()
    return render_template("readCourses.html",
                            cfg = cfg,
                            courses = courses)