from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser


@app.route("/admin/programManagement/<pid>", methods=["GET", "POST"])
def adminProgramManagement(pid):
  # if (request.method == "GET"):
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin():
      users = User.select().order_by(User.lastName)
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
                              isAdmin       = authorizedUser.isAdmin())
    else:
        return render_template("404.html", cfg=cfg)