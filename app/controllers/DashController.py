# Dashboard Controller

from app import app
from app.models import *

from flask import \
    render_template, \
    redirect, \
    request

@app.route('/dashboard/', methods=["GET"])
def dash():
    working = Ta.select()\
            .join(User, on=(Ta.uID_id == User.uID))\
            .where(Ta.working == 1)
    return render_template('index.html',
                           working = working)
