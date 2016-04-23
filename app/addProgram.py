from allImports import *


@app.route("/admin/newProgram", methods=["GET", "POST"])
def addProgram():
  if (request.method == "GET"):
      username = authUser(request.environ)
      admin = User.get(User.username == username)
      if admin.isAdmin:
         users = User.select()
         divisions = Division.select()
         programs  = Program.select()
         
         return render_template("newProgram.html",
                                 cfg           = cfg,
                                 users         = users,
                                 divisions     = divisions,
                                 programs      = programs,
                                 isAdmin       = admin.isAdmin)
  if (request.method == "POST"):
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if admin.isAdmin:
      data = request.form
      professors = request.form.getlist('professors[]')
      program = Program(name = data['programName'], division = data['division'])
      program.save()
      for professor in professors:
        newProgramChair = ProgramChair(username = professor, pid = program.pID)
        newProgramChair.save()
    flash("Program added successfully")
    return redirect(url_for("admin/ProgramManagement", pid = program.pID))