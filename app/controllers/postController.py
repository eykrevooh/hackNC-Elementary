#Post question controller

from app.allImports import *
from app.watson_api import Watson

@app.route('/post/', methods=["GET","POST"])
@app.route('/post/<perm>', methods=["GET","POST"])
def postQuestion(perm=None):
    if request.method == "POST":
        title = request.form["title"]
        quest = request.form["question"]
        course = request.form["courses"]

        myWatson = Watson()
        myWatson.set_username(cfg['watson']['conversation'],\
                                cfg['watson']['translator'])
        lang = myWatson.identify_lang(quest)
        quest = myWatson.translate(quest, lang, "en")
        
        cId = Course.select().where(Course.course_num == course).get()
        Question(
             sID = 1,
             cID = cId,
             status = "PENDING",
             assignment = "A10",
             title = title,
             question = quest
        ).save()
        question = Question.select(Question.qID)\
                    .where(Question.question == quest)\
                    .get()

        return redirect(url_for('watsonGetQuestion',param = perm, qID = question.qID))
    else:
        courses = Course.select()
        return render_template('postView.html',
                               courses = courses, user=perm)
