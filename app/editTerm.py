from allImports import *
from app.logic.getAuthUser import AuthorizedUser
@app.route("/editTerm", methods=["POST"])
def editterm():
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin():
      page =  "/" + request.url.split("/")[-1]
      data = request.form
      term = Term.get(Term.termCode == data['termCode'])
      term.editable = not term.editable
      term.save()
        
      message = "Term: term {} has been made editable".format(data['termCode'])
      log.writer("INFO", page, message)
      return redirect(url_for("systemManagement"))