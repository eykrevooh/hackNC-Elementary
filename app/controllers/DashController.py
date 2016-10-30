# Dashboard Controller

from app import app
from app.models import *

from flask import \
    render_template, \
    redirect, \
    request

@app.route('/dashboard/<perm>', methods=["GET"])
def dash(perm):
    print perm
    working = Ta.select()\
            .join(User, on=(Ta.uID_id == User.uID))\
            .where(Ta.working == 1)
    return render_template('dash.html',
                           working = working,user=perm)
