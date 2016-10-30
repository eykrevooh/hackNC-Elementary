# Questions Controller

from app.allImports import *

from flask import jsonify, redirect

@app.route('/questions/<user>/', methods=["GET"])
def questions(user):
    questions = Question.select()
    classes = Course.select()
    #two queries 2) all questions NOT associated with 'signed in user' and 1) all questions ONLY associated with 'signed in user'
    return render_template('questionsView.html',
                           questions = questions,
                           classes = classes,
                           user = user)

@app.route('/claim/', methods=["GET"])
def claim():
    username = request.args.get('user')
    question = request.args.get('question')

    user = User.get(User.username == username)
    questionThing = Question.get(Question.qID == question)

    questionThing.taID_id = user
    questionThing.update()

    return jsonify({'result': 'success'})

@app.route('/resolve/', methods=['GET'])
def resolve():
    question = request.args.get('question')
    user = request.args.get('user')

    questionQuery = Question.get(Question.qID == question)

    questionQuery.delete_instance()

    return redirect("/questions/%s/" %(user))
