from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser


@app.route("/admin/divisionManagement/<did>", methods=["GET", "POST"])
def adminDivisionManagement(did):
  if (request.method == "GET"):
      authorizedUser = AuthorizedUser()
      if authorizedUser.isAdmin():
         users = User.select()
         divisions = Division.select()
         division = Division.get(Division.dID == did)
         divisionChairs = {}
         divisionChairs[division.dID] = DivisionChair.select().where(DivisionChair.did == division.dID)
         
         return render_template("editDivision.html",
                                 division      = division,
                                 divisionChairs = divisionChairs,
                                 cfg           = cfg,
                                 users         = users,
                                 divisions     = divisions,
                                 isAdmin       = authorizedUser.isAdmin)