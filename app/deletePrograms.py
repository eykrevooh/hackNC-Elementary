from allImports import *

@app.route("/deletePrograms/<pid>", methods=["GET"])

def deleteProgram(pid):
    page = request.path
    program = Programs.get(Programs.pid==pid)
    log.writer("INFO", page, "This is another test of a log in the deletePrograms file")
    program.delete_instance()
    program.save()
    return redirect(url_for("readPrograms"))
