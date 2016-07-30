from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.excelMaker import makeExcelFile
from flask import send_file
@app.route("/excel/<tid>", methods=["GET"])
def makeExcel(tid):
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin():
      
      page        = "/" + request.url.split("/")[-1]
      term = Term.get(Term.termCode == tid)
      makeExcelFile(term)
      return send_file('/home/ubuntu/workspace/cas-{}-courses.xlsx'.format(tid),as_attachment=True)
        
    #   flash("Division succesfully changed")
    #   return redirect(redirect_url())