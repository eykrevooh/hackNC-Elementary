from allImports import *
from updateCourse import DataUpdate


@app.route("/admin/programManagement/<pid>", methods=["GET", "POST"])
def adminProgramManagement(pid):
  # if (request.method == "GET"):
   username = authUser(request.environ)
   admin = User.get(User.username == username)
   if admin.isAdmin:
      users = User.select()
      divisions = Division.select()
      programs  = Program.select()
      program = Program.get(Program.pID == pid)
      programChairs = {}
      programChairs[program.pID] = ProgramChair.select().where(ProgramChair.pid == program.pID)
      
      return render_template("editProgram.html",
                              program       = program,
                              programChairs = programChairs,
                              cfg           = cfg,
                              users         = users,
                              divisions     = divisions,
                              programs      = programs,
                              isAdmin       = admin.isAdmin)
   