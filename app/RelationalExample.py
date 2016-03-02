from allImports import *

@app.route("/aRelationalTable", methods=["GET", "POST"])
def aRelationalQuery():
  users = Users.select()
  return render_template("aRelationalTable.html",
                         cfg = cfg,
                         users = users)
