from __future__ import print_function
import os
from flask import Flask
from flask import render_template
from view import *

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

if __name__ == "__main__":
  if os.getenv('IP'):
    IP = os.getenv('IP')
  else:
    IP = '0.0.0.0'
  
  if os.getenv('PORT'):
    PORT = int(os.getenv('PORT'))
  else:
    PORT = 8080
  
  print ("Running at http://{0}:{1}/".format(IP, PORT))
  app.run(host = IP, port = PORT, debug = True, threaded = True)
  