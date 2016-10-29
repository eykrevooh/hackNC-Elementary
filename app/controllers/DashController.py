# Dashboard Controller

from app import app
from app.models import *

from Flask import \
    render_template, \
    redirect, \
    request

@app.route('/dash/', methods=["GET"])
def dash():
    working = Ta.select().where(working = 1)
    return render_template('dashView.html',
                           working = working)
