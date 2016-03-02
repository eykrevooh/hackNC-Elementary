# this renders the home page which is start.html
from allImports import *
@app.route("/", methods = ["GET"])
def start():
  return render_template("start.html",
                          cfg = cfg)