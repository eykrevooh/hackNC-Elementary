from allImports import *


@app.route("/home", methods=["GET", "POST"])
def home():
  if (request.method == "GET"):
      terms = Term.select()
      return render_template("courseLanding.html",
                            cfg      = cfg,
                            terms = terms
                          )
  data   = request.form
  termId = data["termSelect"]
  return redirect(url_for("home", tID = termId))
  