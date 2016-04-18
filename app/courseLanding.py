from allImports import *


@app.route("/home/<username>", methods=["GET", "POST"])
def home(username):
  if (request.method == "GET"):
      terms = Term.select()
      return render_template("courseLanding.html",
                            cfg      = cfg,
                            terms = terms
                          )
  data       = request.form
  termId     = data["termSelect"]
  username   = authUser(request.environ)
  myProgram  = User.get(User.username == username)
  return redirect(url_for("courses", tID = termId, prefix = "AFR"))
  