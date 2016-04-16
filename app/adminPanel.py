from allImports import *
from updateCourse import DataUpdate


@app.route("/admin", methods=["GET", "POST"])
def admin():
  if (request.method == "GET"):
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    terms = Term.select()
    if admin.isAdmin:
      programs = Program.select()
      
      programChairs = {}
      for program in programs:
        programChairs[program.pID] = ProgramChair.select().where(ProgramChair.pid == program.pID)
        
      divisions = Division.select()
      
      divisionChairs = {}
      for division in divisions:
        divisionChairs[division.dID] = DivisionChair.select().where(DivisionChair.did == division.dID) 
      
      users = User.select().order_by(User.firstName)
    
    
      return render_template("adminPanel.html",
                              programs=programs,
                              programChairs = programChairs,
                              divisions = divisions,
                              divisionChairs = divisionChairs,
                              terms = terms,
                              cfg = cfg,
                              users = users)
                              
                              
    return render_template("404.html", cfg=cfg)
                              
  