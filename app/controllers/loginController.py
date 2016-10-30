# Login Controller

from app.allImports import *

@app.route('/', methods=["GET","POST"])
def homeReroute():
    return redirect("/login/")

@app.route('/login/', methods=["GET", "POST"])
def login():
    print request.method
    if request.method == "POST": 
        username = request.form["username"]
        working = Ta.select()\
                .join(User, on=(Ta.uID_id == User.uID))\
                .where(Ta.working == 1)
        if username == "ta1":
            if Ta.select().where(Ta.working == 1).count() > 1:
                kye = Ta.get(Ta.working == 1)
                kye.working = 0
                kye.save()
            return redirect(url_for('dash',perm=username))
        elif username == "stu1":
           return redirect(url_for('dash',perm=username))
        else:
            return render_template('loginView.html', user = None)
    else:
        return render_template('loginView.html', user = None)
