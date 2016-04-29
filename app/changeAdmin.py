from allImports import *
@app.route("/changeAdmin", methods=["POST"])
def changeAdmin():
  page = request.path
  username = authUser(request.environ)
  admin = User.get(User.username == username)
  if admin.isAdmin:
    data = request.form
    print data
    user = User.get(User.username == data['admin'])
    user.isAdmin = not user.isAdmin
    user.save()
    
    #log changes
    message = "User: {0} is now {1} an admin".format(user.username, (lambda:"not", lambda:"")[user.isAdmin]())
    log.writer("INFO", page, message)
    
    flash("Administrator successfully added")
    return redirect(url_for('systemManagement'))
  else:
    log.writer("ERROR", page, log.lowPrivilege)
    return render_template("404.html")