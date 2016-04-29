from __future__ import print_function
'''
Include all imports in this file; it will be called at the beginning of all files.
'''
# We need a bunch of Flask stuff
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import g
from flask import url_for
from flask import flash
from flask import abort


import pprint
from app import models

from models import *                # all the database models
from app.switch import switch       # implements switch/case statements




''' Creates an Flask object; @app will be used for all decorators.
from: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
"A decorator is just a callable that takes a function as an argument and 
returns a replacement function. See start.py for an example"
'''
def authUser(env):
  envK = "eppn"  
  # app.logger.info("Found remote user: " + env.get("HTTP_X_REMOTE_USER") + env.get("PHP_AUTH_USER"))
  if (envK in env):
    # print("We're live"+  env[envK].split("@")[0]+ ";")
    return env[envK].split("@")[0]
  elif ("DEBUG" in app.config) and app.config["DEBUG"]:
    # print("We're in debug: " + cfg["DEBUG"]["user"])
    return cfg["DEBUG"]["user"]
  else:
    return None
    
from app import logtool
log = logtool.Log()

app = Flask(__name__)
app.secret_key = "SUPER DUPER SECRET KEY"
# Builds all the database connections on app run
# Don't panic, if you need clarification ask.
@app.before_request
def before_request():
    g.dbMain =  mainDB.connect()

@app.teardown_request
def teardown_request(exception):
    dbM = getattr(g, 'db', None)
    if (dbM is not None) and (not dbM.is_closed()):
      dbM.close()
