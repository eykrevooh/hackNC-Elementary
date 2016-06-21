#ADD ANY IMPORTS HERE
from allImports import *


#GRAB THE URL HERE
@app.route("/conflicts", methods = ["GET", "POST"])
def conflicts():
    username = authUser(request.environ)

    #RETURN THE HTML AND PASS THE NECESSARY DATA    
    return render_template("conflicts.html",
                            cfg = cfg
                          )