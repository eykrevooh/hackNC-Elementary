from allImports import *
@app.route("/editTerm", methods=["POST"])
def editterm():
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if admin.isAdmin:
      page = request.page
      data = request.form
      term = Term.get(Term.termCode == data['termCode'])
      term.editable = not term.editable
      term.save()
        
      message = "Term: term {} has been editable".format(data['termCode'])
      log.writer("INFO", page, message)