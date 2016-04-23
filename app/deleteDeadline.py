from allImports import *
@app.route("/deleteDeadline", methods=["POST"])
def deleteDeadline():
   username = authUser(request.environ)
   admin = User.get(User.username == username)
   if admin.isAdmin:
      data = request.form
      deadline = Deadline.get(Deadline.id == int(data['id']))
      deadline.delete_instance()
   return redirect(url_for("deadlineDisplay"))