from allImports import *
@app.route("/newTerm", methods=["POST"])
def newterm():
  page = request.path  
  username = authUser(request.environ)
  admin = User.get(User.username == username)
  if admin.isAdmin:
    data = request.form
    term = Term(termCode = int(data['termCode']), name = data['termName'], editable = True)
    term.save()
  message = "Term: Term {} has been created".format(data['termCode'])
  log.writer("INFO", page, message)
  flash("Term successfully created")
  return redirect(url_for("systemManagement"))