#Post question controller

from app import app
from app.models import *

from flask import \
    render_template, \
    redirect, \
    request

@app.route('/post/', methods=["GET","POST"])
def postQuestion():
    if request.method == 'POST':
        #TODO: set values posted by form for question table
        pass
    return render_template('postView.html')
