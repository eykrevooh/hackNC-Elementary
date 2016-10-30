import json
from random import choice
from watson_developer_cloud import ConversationV1, LanguageTranslatorV2 as LT

class Watson:
    def __init__(self):
        self.user = None
        self.password = None
        self.workspace_id = None 
        self.ans_header = ["It's a good question.", "Great question!", "That was a difficult one."]
        self.not_found = "I'm sorry I don't understand, but I have notified the TA."
        

    def set_username(self, auth1, auth2):
        self.conversation = ConversationV1(
          username = auth1[0],
          password = auth1[1],
          version = '2016-09-20'
        )
        self.workspace_id = auth1[2]
        self.lt = LT(
            username = auth2[0],
            password = auth2[1]
        )

    def ask_question(self, question):
        context = dict()
        response = self.conversation.message(
          workspace_id= self.workspace_id,
          message_input={'text': question},
          context=context
        )
        return response

    def parse_response(self, res):
        watson_ans = res["output"]["text"][0]
        if watson_ans != self.not_found:
            return "{0} {1}".format(choice(self.ans_header), watson_ans)
        return watson_ans

    def identify_lang(self, text):
        language = self.lt.identify(text)
        return language["languages"][0]["language"]
    
    def translate(self, text, src, trgt):
        translation = self.lt.translate(
                text = text, 
                source = src,
                target = trgt
                )
        print type(translation)
        return str(translation)

def main():
    auth1 = ("8a9ded6d-8130-4d2f-938a-77299633e497", "sFqr0eofA22w", "1e9c006c-5435-43fd-9921-30c5ff96ee16")
    auth2 = ("4454222a-b333-48e6-a8ee-0e7d5aa8a929", "sJkfneX7xR6e") 
    watson = Watson()
    watson.set_username(auth1, auth2)
    while True:
        question = raw_input("What's your question: ")
        lang = watson.identify_lang(question)
        translation = watson.translate(question, str(lang), "en")
        print translation
        response = watson.ask_question(translation)
        print watson.parse_response(response)
main()
