#Questions Controller

from app import app
from app.models import *

from Flask import \
    render_template, \
    redirect, \
    request

@app.route('/questions/<user>/', methods=["GET"])
def questions(user):
    claimedQs = questions.select().where(questions.taId == user)
    unclaimedQs = questions.select().where(questions.taId != user) 
    #two queries 2) all questions NOT associated with 'signed in user' and 1) all questions ONLY associated with 'signed in user'
    return render_template('questionsView.html',
                           user      =     user)
