# Dashboard Controller

from app import app
from app.models import *

from flask import \
    render_template, \
    redirect, \
    request

@app.route('/dash/', methods=["GET"])
def dash():
    working = Ta.select().where(Ta.working == 1)
    return render_template('dashView.html',
                           working = working)
