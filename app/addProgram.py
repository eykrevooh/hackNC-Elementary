from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.databaseInterface import createProgram, addProgramChairs


@app.route("/admin/newProgram", methods=["GET", "POST"])
def addProgram():
    # get username
    username = authUser(request.environ)
    authorizedUser = AuthorizedUser(username)

    page = "/" + request.url.split("/")[-1]
    if (request.method == "GET"):

        if authorizedUser.isAdmin():
          # get elments needed
            users = User.select()
            divisions = Division.select()
            programs = Program.select()

            return render_template("newProgram.html",
                                   cfg=cfg,
                                   users=users,
                                   divisions=divisions,
                                   programs=programs,
                                   isAdmin=authorizedUser.isAdmin())
        else:
          # log error
            log.writer("ERROR", page, log.lowPrivilege)
            return render_template("404.html")

    if (request.method == "POST"):
        # get pag
        page = "/" + request.url.split("/")[-1]
        if authorizedUser.isAdmin():

            # get the data
            data = request.form
            # get the professors

            professors = request.form.getlist('professors[]')

            programName, programID = createProgram(
                data['programName'], data['division'])

            addProgramChairs(professors, programID)

            message = "Program: pid = {0} '{1}' has been added".format(
                programID, programName)
            log.writer("INFO", page, message)

            flash("Program added successfully")

            return redirect(url_for("adminProgramManagement", pid=programID))

        else:

            log.writer("ERROR", page, log.lowPrivilege)

            return render_template("404.html")
