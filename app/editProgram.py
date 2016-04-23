from allImports import *
@app.route("/editProgram", methods=["POST"])
def editProgram():
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if admin.isAdmin:
      data = request.form
      professors = request.form.getlist('professors[]')
      program = Program.get(Program.pID == int(data['programId']))
      program.division = data['division']
      program.name = data['programName']
      program.save()
      oldProgramChairs = ProgramChair.select().where(ProgramChair.pid == int(data['programId']))
      for oldProgramChair in oldProgramChairs:
        if oldProgramChair.username.username not in professors:
          oldProgramChair.delete_instance()
        else:
          professors.remove(oldProgramChair.username.username)
      
      for professor in professors:
        newProgramChair = ProgramChair(username = professor, pid = data['programId'])
        newProgramChair.save()
    flash("Program succesfully changed")
    return redirect(url_for("adminProgramManagement", pid = data['programId']))