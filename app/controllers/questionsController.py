# Questions Controller

from app import app
from app.models import *

from flask import \
    render_template, \
    redirect, \
    request

@app.route('/questions/<user>/', methods=["GET"])
def questions(user):
    claimedQs = Question.select().where(Question.taID == user)
    unclaimedQs = Question.select().where(Question.taID != user) 
    #two queries 2) all questions NOT associated with 'signed in user' and 1) all questions ONLY associated with 'signed in user'
    return render_template('questionsView.html',
                           user = user,
                           claimedQs = claimedQs,
                           unclaimedQs = unclaimedQs)
