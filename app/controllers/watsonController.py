#Post question controller

from app.allImports import *
from app.watson_api import Watson

@app.route('/watson/<qID>', methods=["GET"])
def watsonGetQuestion(qID):
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
                                answer = answer)
