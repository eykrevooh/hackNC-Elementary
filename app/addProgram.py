from allImports import *


@app.route("/admin/newProgram", methods=["GET", "POST"])
def addProgram():
  page = "/" + request.url.split("/")[-1]
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
      else:
        log.writer("ERROR", page, log.lowPrivilege)
        return render_template("404.html")
      
  if (request.method == "POST"):
    page = "/" + request.url.split("/")[-1]
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
      message = "Program: pid = {0} '{1}' has been added".format(program.pID ,program.name)
      log.writer("INFO", page, message)
      flash("Program added successfully")
      return redirect(url_for("adminProgramManagement", pid = program.pID))
    else:
      log.writer("ERROR", page, log.lowPrivilege)
      return render_template("404.html")
      
    
    