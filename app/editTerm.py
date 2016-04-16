from allImports import *
@app.route("/editTerm", methods=["POST"])
def editterm():
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if admin.isAdmin:
      data = request.form
      term = Term.get(Term.termCode == data['termCode'])
      term.editable = not term.editable
      term.save()
        
    return "hello"