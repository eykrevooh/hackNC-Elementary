from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.databaseInterface import addDivisionChairs, createDivision


@app.route("/admin/newDivision", methods=["GET", "POST"])
def addDivision():
    # get the page
    page = "/" + request.url.split("/")[-1]
    username = authUser(request.environ)
    authorizedUser = AuthorizedUser(username)

    if (request.method == "GET"):
        

        if authorizedUser.isAdmin():
            # get the users
            users = User.select()
            # get divisions
            divisions = Division.select()
            # get programs
            programs = Program.select()

            return render_template("newDivision.html",
                                   cfg=cfg,
                                   users=users,
                                   divisions=divisions,
                                   programs=programs,
                                   isAdmin=authorizedUser.isAdmin())

        else:
            log.writer("ERROR", page, log.lowPrivilege)
            return render_template("404.html")

    if (request.method == "POST"):

        if authorizedUser.isAdmin():
            # get the data
            data = request.form

            # get the professor list
            professors = request.form.getlist('professors[]')

            # create division in database
            divisionName, divisionID = createDivision(data['divisionName'])

            # add professors to the database
            addDivisionChairs(professors, divisionID)

            # log successful queries
            message = "Division: {0} has been added".format(divisionName)
            log.writer("INFO", page, message)

            flash("Division added successfully")
            return redirect(url_for("adminDivisionManagement", did=divisionID))

        else:
            log.writer("ERROR", page, log.lowPrivilege)
            return render_template("404.html")
