# Login Controller

from app import app
from app.models import *

from Flask import \
    render_template, \
    redirect, \
    request

@app.route('/', methods=["GET","POST"])
def homeReroute():
    return redirect("/login/")

@app.route('/login/', methods=["GET", "POST"])
def login():
    #Dummy form that just passes the username because we don't feel like actually implementing a login system
    return render_template('loginView.html')
