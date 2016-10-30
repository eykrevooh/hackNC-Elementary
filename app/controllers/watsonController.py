#Post question controller

from app.allImports import *
from app.watson_api import Watson

@app.route('/watson/<qID>', methods=["GET"])
@app.route('/watson/<qID>/<param>', methods=["GET"])
def watsonGetQuestion(qID,param="ta1"):
    if request.method == "GET":
        
        question = Question.select()\
                    .where(Question.qID == qID)\
                    .get()
        myWatson = Watson()
        myWatson.set_username(cfg['watson']['conversation'],\
                                cfg['watson']['translator'])
        res = myWatson.ask_question(question.question)
        answer = myWatson.parse_response(res)
        return render_template('watsonView.html',\
                                question = question,\
                                answer = answer,
                                user = param)
    else:
        courses = Course.select()
        return render_template('postView.html',
                               courses = courses,
                               user = param)
