from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
@app.route("/editTerm", methods=["POST"])
def editterm():
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin():
      page =  "/" + request.url.split("/")[-1]
      data = request.form
      term = Term.get(Term.termCode == data['termCode'])
      term.editable = not term.editable
      term.save()
      
      editability = "not editable"  
      if term.editable:
        editability = "editable"
      message = "Term: term {0} has been made {1}".format(data['termCode'], editability)
      log.writer("INFO", page, message)
      return redirect(redirect_url())