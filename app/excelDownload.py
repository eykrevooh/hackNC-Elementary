from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.excelMaker import makeExcelFile
from flask import send_file
from os.path import basename
import os

@app.route("/excel/<tid>", methods=["GET"])
def makeExcel(tid):
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin():
      
      page        = "/" + request.url.split("/")[-1]
      term = Term.get(Term.termCode == tid)
      completePath = makeExcelFile(term)
      
      #filename = "cas-{}-courses.xlsx".format(tid)
      #currentLocation = os.path.dirname(os.path.dirname(__file__))
      #currentLocation = os.path.join(currentLocation, "data/tmp")
      #completePath = os.path.join(currentLocation, filename)
      #print completePath
      #completePath = filename
      
      return send_file(completePath,as_attachment=True)
      
        
    #   flash("Division succesfully changed")
    #   return redirect(redirect_url())