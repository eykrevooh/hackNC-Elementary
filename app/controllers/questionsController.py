# Questions Controller

from app.allImports import *

@app.route('/questions/<perm>', methods=["GET"])
def questions(perm):
    questions = Question.select()
    print questions
    classes = Course.select()
    #two queries 2) all questions NOT associated with 'signed in user' and 1) all questions ONLY associated with 'signed in user'
    return render_template('questionsView.html',
                           questions = questions,
                           classes = classes,
                           user = perm)

@app.route('/claim/', methods=["GET"])
def claim():
    username = request.args.get('user')
    question = request.args.get('question')

    user = User.get(User.username == username)
    questionThing = Question.get(Question.qID == question)

    questionThing.taID = user
    questinThing.save()

    return 0
