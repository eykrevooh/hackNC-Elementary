from allImports import *
@app.route("/editDivision", methods=["POST"])
def editDivision():
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if admin.isAdmin:
      data = request.form
      professors = request.form.getlist('professors[]')
      division = Division.get(Division.dID == int(data['divisionId']))
      
      division.name = data['divisionName']
      division.save()
      
      oldDivisionChairs = DivisionChair.select().where(DivisionChair.did == int(data['divisionId']))
      for oldDivisionChair in oldDivisionChairs:
        if oldDivisionChair.username not in professors:
          oldDivisionChair.delete_instance()
        else:
          professors.remove(oldDivisionChair.username.username)
      
      for professor in professors:
        newDivisionChair = DivisionChair(username = professor, did = data['divisionId'])
        newDivisionChair.save()
        
    return "hello"