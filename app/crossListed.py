#ADD ANY IMPORTS HERE
from allImports import *
from updateCourse import DataUpdate

#GRAB THE URL HERE
@app.route("/crossListed", methods=["GET", "POST"])
def crossListed():
    X = 0

    #RETURN THE HTML AND PASS THE NECESSARY DATA    
    return render_template("crossListed.html",
                            cfg = cfg
                          )