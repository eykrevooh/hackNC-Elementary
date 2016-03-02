'''
  fileName: readPrograms.py
  Purpose:
            Handles the preprocessing that needs to be done for page1.html
            Also, is another example of how to build web pages

'''

from allImports import *

@app.route("/readPrograms" , methods = ["GET"])

def readPrograms():
  """This function will get data from the database"""
  programs = (Programs.select()) #This is what a database query looks like
  return render_template( "readPrograms.html",
                            cfg = cfg, 
                            programs = programs
                          )
#Make sure to create the html inside of templates
#Make sure to place from app import page1 inside of __init__.py so that initilizer knows whats in the module