from allImports import *

@app.route("/deletePrograms/<pid>", methods=["GET"])

def deleteProgram(pid):
    program = Programs.get(Programs.pid==pid)
    program.delete_instance()
    program.save()
    return redirect(url_for("readPrograms"))
