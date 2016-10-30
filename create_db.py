# WARNING: NOT FOR USE IN PRODUCTION AFTER REAL DATA EXISTS!!!!!!!!!!!!!!!!!!!!!!
'''
This script creates the database tables in the SQLite file. 
Update this file as you update your database.
'''
import os, sys
import importlib
import datetime

# Don't forget to import your own models!
from app.models import *
conf = load_config(os.path.join(here,'config.yaml'))
#onf = load_config('app/config.yaml')

sqlite_dbs  = [ conf['databases']['dev']
                # add more here if multiple DBs
              ]

# Remove DBs
for fname in sqlite_dbs:
  try:
    print ("Removing {0}.".format(fname))
    os.remove(fname)
  except OSError:
    pass

# Creates DBs
for fname in sqlite_dbs:
  if os.path.isfile(fname):
    print ("Database {0} should not exist at this point!".format(fname))
  print ("Creating empty SQLite file: {0}.".format(fname))
  open(fname, 'a').close()
  

def class_from_name (module_name, class_name):
  # load the module, will raise ImportError if module cannot be loaded
  # m = __import__(module_name, globals(), locals(), class_name)
  # get the class, will raise AttributeError if class cannot be found
  c = getattr(module_name, class_name)
  return c
    
"""This file creates the database and fills it with some dummy run it after you have made changes to the models pages."""
def get_classes (db):
  classes = []
  for str in conf['models'][db]:
    print ("\tCreating model for '{0}'".format(str))
    c = class_from_name(sys.modules[__name__], str)
    classes.append(c)
  return classes
  
mainDB.create_tables(get_classes('mainDB'))

User(username = "ta4",
     name     = "Jesson Soto Ventrua",
     password = "1234",
     role     = 0,
     year     = 7,
     sex      = 0,
     race     = "Cacuasian").save()

User(username = "ta1",
     name     = "Kye Hoover",
     password = "1234",
     role     = 1,
     year     = 4,
     sex      = 1,
     race     = "African-American").save()

User(username = "ta2",
     name     = "Zach Ball",
     password = "1234",
     role     = 1,
     year     = 3,
     sex      = 0,
     race     = "Asian").save()

User(username = "ta3",
     name     = "Ishwar Agarwal",
     password  = "1234",
     role      = 1,
     year      = 3,
     sex       = 0,
     race      = "Asian").save()


User(username = "stu1",
     name     = "Steve Morris",
     password = "1234",
     role     = 2,
     year     = 1,
     sex      = 1,
     race     = "Cacuasian").save()

User(username = "stu2",
     name     = "John Hellfung",
     password = "1234",
     role     = 2,
     year     = 7,
     sex      = 0,
     race     = "Asian").save()

Ta(  uID = 2,
     bio = "Senior Computer Science major",
     pict = "/static/photos/sexy_kye.jpg",
     working = 1).save()

Ta(  uID = 3,
     bio = "Senior Computer Science major, expert in Asp.net",
     pict = "/static/photos/sexy_zach.jpg",
     working = 1).save()

Ta(  uID = 4,
     bio = "Junior Computer Science major, expert in Asp.net",
     pict = "/static/photos/sexy_ishwar.jpg",
     working = 1).save()

Ta(  uID = 1,
     bio = "Sophmore Computer Science major, expert in Asp.net",
     pict = "/static/photos/sexy_jesson.jpg",
     working = 1).save()

Student(uID = 4,
        need_help = 1).save()

Student(uID = 5,
        need_help = 0).save()

Course( course_num = "CSC 236",
        course_title = "Software Engineering",
        course_dec = "An intorduction the implementation of full stack engineering",
        python = True,
        c = False,
        cplus = False,
        c_sharp = False,
        java = False,
        racket = True,
        haskell = False).save()

Course( course_num = "CSC 486",
        course_title = "Programming Languages",
        course_dec = "Learn a variety of programming languages and develop your own in Racket",
        python = True,
        c = False,
        cplus = False,
        c_sharp = False,
        java = False,
        racket = True,
        haskell = False).save()

Question(
        sID = 1,
        cID = 1,
        status = "PENDING",
        assignment = "A10",
        title = "Linked List Issue",
        question = "Kye is tired and is not thinking of a question").save()

Question(
        sID = 1,
        cID = 1,
        status = "PENDING",
        assignment = "A10",
        title = "Strange numbers on printf",
        question = "When I try to print a variable with printf, I am only seeing a hexidecimal number.").save()

Question(
        sID = 1,
        cID = 2,
        status = "PENDING",
        assignment = "L4",
        title = "Can't compile code",
        question = "My code won't compile").save()


SCRelation(
        sID = 1,
        cID = 1).save()

SCRelation(
        sID = 2,
        cID = 1).save()

SCRelation(
        sID = 1,
        cID = 2).save()

TaCRelation(
        taID = 1,
        cID = 2).save()

TaCRelation(
        taID = 2,
        cID = 1).save()

TaCRelation(
        taID = 2,
        cID = 2).save()

print "Database populated with values"
