from allImports import *


@app.route("/admin/newDivision", methods=["GET", "POST"])
def addDivision():
  page = request.path
  if (request.method == "GET"):
      username = authUser(request.environ)
      admin = User.get(User.username == username)
      if admin.isAdmin:
        users = User.select()
        divisions = Division.select()
        programs  = Program.select()
         
        return render_template("newDivision.html",
                                 cfg           = cfg,
                                 users         = users,
                                 divisions     = divisions,
                                 programs      = programs,
                                 isAdmin       = admin.isAdmin)
      else:
        log.writer("ERROR", page, log.lowPrivilege)
        return render_template("404.html")
  
  if (request.method == "POST"):
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    
    
    if admin.isAdmin:
      data = request.form
      professors = request.form.getlist('professors[]')
      division = Division(name = data['divisionName'])
      division.save()
      for professor in professors:
        newDivisionChair = DivisionChair(username = professor, did = division.dID)
        newDivisionChair.save()
      
      # log successful queries
      message = "Division: {0} has been added".format(division.name)
      log.writer("INFO", page, message)
        
      flash("Division added successfully")
      return redirect(url_for("adminDivisionManagement", did = division.dID))
    
    else:
      log.writer("ERROR", page, log.lowPrivilege)
      return render_template("404.html")
  