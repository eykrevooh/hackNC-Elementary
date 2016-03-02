from allImports import *


@app.route("/editPrograms/<pid>", methods=["GET", "POST"])
def page2(pid):
  program = Programs.get(Programs.pid == pid)
  if (request.method == "GET"):
    return render_template("editPrograms.html",
                            cfg      = cfg,
                            program = program
                          )
  data = request.form
  program.programName   = data['programName'] 
  program.abbreviation  = data['abb']
  program.save()
  return redirect(url_for("readPrograms"))
  