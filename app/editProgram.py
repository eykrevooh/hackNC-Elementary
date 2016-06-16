from allImports import *
@app.route("/editProgram", methods=["POST"])
def editProgram():
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if admin.isAdmin:
      page        = "/" + request.url.split("/")[-1]
      data        = request.form
      newChairs   = request.form.getlist('professors[]')
      pid         = data['pID']
      
      currentChairs = ProgramChair.select().where(ProgramChair.pid == pid)  #SELECT ALL OF THE CURRENT CHAIRS OF THE PROGRAM
      for currentChair in currentChairs:                                    #LOOP THROUGH ALL OF THE CURRENT CHAIRS
        if currentChair.username.username not in newChairs:                 #IF A USER'S NAME IS NOT PART OF THE NEWCHAIR LIST THEN DELETE THEM
          message = "USER: {0} has been removed as a program chair for pid: {1}".format(currentChair.username.username,pid)
          log.writer("INFO", page, message)
          currentChair.delete_instance()
        else:
          newChairs.remove(currentChair.username.username)                  #HOWEVER IF THEY ARE PART OF THE LIST, DELETE THEM FROM THE LIST
          
      for user_name in newChairs:                                           #LOOK THROUGH THE NEW CHAIR LIST
        newChair  = ProgramChair(username = user_name, pid = pid)           #ADD THE USERNAMES TO THE PROGRAM CHAIR LIST
        newChair.save()                                                     
        message = "USER: {0} has been added as a program chair for pid: {1}".format(user_name,pid)
        log.writer("INFO", page, message)
        
      flash("Program succesfully changed")
      return redirect(url_for("adminProgramManagement", pid = pid))
        
      
        

     
    
   