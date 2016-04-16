from allImports import *
@app.route("/newTerm", methods=["POST"])
def newterm():
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if admin.isAdmin:
      data = request.form
      term = Term(termCode = int(data['termCode']), name = data['termName'], editable = True)
      term.save()
        
    return "hello"