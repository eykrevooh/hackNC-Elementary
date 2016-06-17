from allImports import *
@app.route("/changeAdmin", methods=["POST"])
def changeAdmin():
  page = "/" + request.url.split("/")[-1]
  username = authUser(request.environ)
  admin = User.get(User.username == username)
  if admin.isAdmin:
    data = request.form
    if data['admin'] != "None":
      user = User.get(User.username == data['admin'])
      user.isAdmin = not user.isAdmin
      user.save()
      #log changes
      message = "User: {0} is now {1} an admin".format(user.username, (lambda:"not", lambda:"")[user.isAdmin]())
      log.writer("INFO", page, message)
      if "not" in message:
        flash("Administrator {0} {1} successfully removed".format(user.firstName, user.lastName))
      else:
        flash("Administrator {0} {1} successfully added".format(user.firstName, user.lastName))
      if username == data['admin']: #IF THE USER DELETES THEMSELVES SEND THEM BACK TO THE HOME PAGE
        return redirect('/')
      else:
        return redirect(url_for('systemManagement'))
    else:
      message = "A username was not selected during the process."
      log.writer("INFO", page, message)
      flash(message)
      return redirect(url_for('systemManagement'))
  else:
    log.writer("ERROR", page, log.lowPrivilege)
    return render_template("404.html")