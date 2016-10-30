# Questions Controller

from app import app
from app.models import *

from flask import \
    render_template, \
    redirect, \
    request

@app.route('/questions/', methods=["GET"])
def questions():
    questions = Question.select()
    classes = Course.select()
    #two queries 2) all questions NOT associated with 'signed in user' and 1) all questions ONLY associated with 'signed in user'
    return render_template('questionsView.html',
                           questions = questions,
                           classes = classes)
