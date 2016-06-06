from allImports import *
@app.route("/newTerm", methods=["POST"])
def newterm():
  page = request.path  
  username = authUser(request.environ)
  admin = User.get(User.username == username)
  try: 
    if admin.isAdmin:
      data = request.form
      newterm = Term(termCode = int(data['termCode']), name = data['termName'], editable = True)
      newterm.save(force_insert=True)
  except Exception as e:
    log.writer("ERROR","newTerm",e)
  message = "Term: Term {} has been created".format(data['termCode'])
  log.writer("INFO", page, message)
  flash("Term successfully created")
  return redirect(url_for("systemManagement"))