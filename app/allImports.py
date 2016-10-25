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
from flask_admin import Admin
import time
import sys,os

import pprint
from app import models
# all the database models
from models import *     


''' Creates an Flask object; @app will be used for all decorators.
from: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
"A decorator is just a callable that takes a function as an argument and
returns a replacement function. See start.py for an example"
'''


def authUser(env):
    envK = "eppn"
    if (envK in env):
        return env[envK].split("@")[0]
    elif ("DEBUG" in app.config) and app.config["DEBUG"]:
        return cfg["DEBUG"]["user"]
    else:
        return None

'''Creates the AbsolutePath based off of the relative path.
Also creates the directories in path if they are not found.
@param {string} relaitivePath - a string of directories found in config.yaml
@param {string} filename - the name of the file that should be in that directory
@return {string} filepath -returns the absolute path of the directory'''
'''TODO: ADD @PARAm for make dirs'''
def getAbsolutePath(relaitivePath,filename):
    filepath = os.path.join(sys.path[0],relaitivePath)
    try:
        os.makedirs(filepath)
    except:
        pass
    if filename != None:
        filepath = os.path.join(filepath,filename)
    return filepath

from app import logtool
log = logtool.Log()

app = Flask(__name__)

app.config.from_object('settings')
# Builds all the database connections on app run
# Don't panic, if you need clarification ask.
admin = Admin(app)



@app.before_request
def before_request():
    g.dbMain = mainDB.connect()


@app.teardown_request
def teardown_request(exception):
    dbM = getattr(g, 'db', None)
    if (dbM is not None) and (not dbM.is_closed()):
        dbM.close()
