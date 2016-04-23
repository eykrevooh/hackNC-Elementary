from allImports import *

@app.route("/redirect/program_management", methods=["GET"])
def redirectProgramManagement():
   program = Program.get()
   
   return redirect(url_for("adminProgramManagement", 
                           pid = program.pID, ))

@app.route("/redirect/division_management", methods=["GET"])
def redirectDivisionManagement():
   division = Division.get()
   
   return redirect(url_for("adminDivisionManagement", 
                           did = division.dID, ))