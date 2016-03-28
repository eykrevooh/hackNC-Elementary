'''
An example first controller. This file does all the pre-processing 
for the index.html page. After pre-processing, it serves the index.html file 
and passes any variables to the templating engine (Jinja) to convert to html
before serving the page to the user.
'''

from allImports import *


# Decorator for the home page (www.myapp.com/)
@app.route("/createPrograms", methods = ["GET" , "POST"])

# The function after the decorator is always run
def firstView():
  page = request.path
  if request.method == "GET": # return a view when request method is GET
    fakeVariable = "Hi"
    # Renders the webpage with the variable fakeVariable being passed to the 
    # templating engine.
    return render_template( "createPrograms.html",
                            fv = fakeVariable,
                            cfg = cfg
                            )
                            
  """Gets the post from the start page"""
  data = request.form #returns a dictionary with all of your post data'
  # line below creates a new entry in the programs table. Check the Database.
  program = Programs(programName = data["progName"], abbreviation = data["abb"])
  log.writer('INFO', page, "This a test log")
  # saves your new object
  program.save()
  return redirect(url_for("readPrograms"))

 
  
