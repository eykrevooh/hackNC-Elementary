from allImports import *
@app.route("/editDivision", methods=["POST"])
def editDivision():
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if admin.isAdmin:
      page        = "/" + request.url.split("/")[-1]
      data        = request.form
      newChairs   = request.form.getlist('professors[]')
      did         = data['dID']
      
      currentChairs = DivisionChair.select().where(DivisionChair.did == did)  #SELECT ALL OF THE CURRENT CHAIRS OF THE DIVISION
      for currentChair in currentChairs:                                      #LOOP THROUGH ALL OF THE CURRENT CHAIRS
        if currentChair.username.username not in newChairs:                   #IF A USER'S NAME IS NOT PART OF THE NEWCHAIR LIST THEN DELETE THEM
          message = "USER: {0} has been removed as a Division chair for did: {1}".format(currentChair.username.username,did)
          log.writer("INFO", page, message)
          currentChair.delete_instance()
        else:
          newChairs.remove(currentChair.username.username)                  #HOWEVER IF THEY ARE PART OF THE LIST, DELETE THEM FROM THE LIST
          
      for user_name in newChairs:                                           #LOOK THROUGH THE NEW CHAIR LIST
        newChair  = DivisionChair(username = user_name, did = did)           #ADD THE USERNAMES TO THE Division CHAIR LIST
        newChair.save()                                                     
        message = "USER: {0} has been added as a Division chair for did: {1}".format(user_name,did)
        log.writer("INFO", page, message)
        
      flash("Division succesfully changed")
      return redirect(url_for("adminDivisionManagement", did = did))