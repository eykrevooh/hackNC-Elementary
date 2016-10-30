import json
from random import choice
from watson_developer_cloud import ConversationV1

class Watson:
    def __init__(self,username, password,workspace_id):
        self.username = username
        self.password = password
        self.workspace_id = workspace_id 
        self.conversation = ConversationV1(
          username = username,
          password = password,
          version = '2016-09-20'
        )
        self.ans_header = ["It's a good question.", "Great question!", "That was a difficult one."]
        self.not_found = "I'm sorry I don't understand, but I have notified the TA."

    def ask_question(self, question):
        context = dict()
        response = self.conversation.message(
          workspace_id= self.workspace_id,
          message_input={'text': question},
          context=context
        )
        print response
        return response

    def parse_response(self, res):
        watson_ans = res["output"]["text"][0]
        if watson_ans != self.not_found:
            return "{0} {1}".format(choice(self.ans_header), watson_ans)
        return watson_ans

def main():
    username = "8a9ded6d-8130-4d2f-938a-77299633e497"
    password = "sFqr0eofA22w"
    workspace_id = "1e9c006c-5435-43fd-9921-30c5ff96ee16"
    watson = Watson(username, password, workspace_id)
    while True:
        question = raw_input("What's your question: ")
        response = watson.ask_question(question)
        print watson.parse_response(response)
main()
