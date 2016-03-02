from peewee import *
import os
#from allImports import *   #Don't believe this import is needed for this file
# Create a database
from app.loadConfig import *

cfg       = load_config('app/config.yaml')
mainDB    = SqliteDatabase(cfg['databases']['dev'])

# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta: 
    database = mainDB

# When adding new tables to the DB, add a new class here (also add 
# to the config.yaml file)
class Programs (dbModel):
  pid           = PrimaryKeyField()
  programName   = TextField()
  abbreviation  = TextField()
  
  
class Users (dbModel):
  uid           = PrimaryKeyField()
  firstName     = TextField()
  lastName      = TextField()
  username      = TextField(unique = True)
  age           = IntegerField(null = True)
  program       = ForeignKeyField(Programs)     # refers to the Programs table by pid
  
class Courses (dbModel):
  cid           = PrimaryKeyField()
  courseName    = TextField()
  coursePrefix  = TextField()
  courseNumber  = IntegerField(null = True)
  pid           = ForeignKeyField(Programs)
  instructor    = ForeignKeyField(Users)