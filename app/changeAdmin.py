from allImports import *
from app.logic.getAuthUser import AuthorizedUser


@app.route("/changeAdmin", methods=["POST"])
def changeAdmin():
    # get page
    page = "/" + request.url.split("/")[-1]

    # get username
    username = authUser(request.environ)

    # autheticator instance
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin():
        # get data
        data = request.form

        if data['admin'] != "None":
            # get the user
            user = User.get(User.username == data['admin'])

            # toggle admin status
            user.isAdmin = not user.isAdmin
            user.save()

            # log changes
            message = "User: {0} is now {1} an admin".format(
                user.username, (lambda: "not", lambda: "")[user.isAdmin]())
            log.writer("INFO", page, message)
            if "not" in message:
                flash(
                    "Administrator {0} {1} successfully removed".format(
                        user.firstName, user.lastName))
            else:
                flash(
                    "Administrator {0} {1} successfully added".format(
                        user.firstName, user.lastName))
                        
            # IF THE USER DELETES THEMSELVES SEND THEM BACK TO THE HOME PAGE
            if username == data['admin']:
                return redirect('/')
            else:
                return redirect(url_for('systemManagement'))
        else:
            message = "A username was not selected during the process."
            log.writer("INFO", page, message)
            flash(message)
            return redirect(url_for('systemManagement'))
    else:
        log.writer("ERROR", page, log.lowPrivilege)
        return render_template("404.html")
