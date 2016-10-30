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
        auth1 = ("8a9ded6d-8130-4d2f-938a-77299633e497", "sFqr0eofA22w", "1e9c006c-5435-43fd-9921-30c5ff96ee16")
        auth2 = ("4454222a-b333-48e6-a8ee-0e7d5aa8a929", "sJkfneX7xR6e") 
        myWatson.set_username(auth1, auth2)
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
