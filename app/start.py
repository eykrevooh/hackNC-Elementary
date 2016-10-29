from allImports import *

@app.route ("/", methods = ["GET"])
def start ():
  return "Hello"
