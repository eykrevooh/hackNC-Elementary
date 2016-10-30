# Login Controller

from app import app
from app.models import *

from flask import \
    render_template, \
    redirect, \
    request, \
    url_for

@app.route('/', methods=["GET","POST"])
def homeReroute():
    return redirect("/login/")

@app.route('/login/', methods=["GET", "POST"])
def login():
    print request.method
    if request.method == "POST": 
        username = request.form["username"]
        print(request.form)
        working = Ta.select()\
                .join(User, on=(Ta.uID_id == User.uID))\
                .where(Ta.working == 1)
        if "ta" in username:
            return redirect(url_for('dash',perm=username))
        elif "stu" in username:
           return redirect(url_for('dash',perm=username))
        else:
            return render_template('loginView.html', user = None)
    else:
        return render_template('loginView.html', user = None)
