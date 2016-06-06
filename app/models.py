from peewee import *
import os

# Create a database
from app.loadConfig import *
here = os.path.dirname(__file__)
cfg       = load_config(os.path.join(here, 'config.yaml'))
mainDB    = SqliteDatabase(cfg['databases']['dev'])

# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta: 
    database = mainDB
    
"""
When adding new tables to the DB, add a new class here 
Also, you must add the table to the config.yaml file

Example of creating a Table

class tableName (dbModel):
  column1       = PrimaryKeyField()
  column2       = TextField()
  column3       = IntegerField()

For more information look at peewee documentation
"""



class Division(dbModel):
  dID           = PrimaryKeyField()
  name          = CharField()

class Program(dbModel):
  pID           = PrimaryKeyField()
  name          = CharField()
  division      = ForeignKeyField(Division)

class User(dbModel):
  username     = CharField(primary_key=True)
  firstName    = CharField()
  lastName     = CharField()
  email        = CharField()
  isAdmin      = BooleanField()
  program      = ForeignKeyField(Program)
  
class Subject(dbModel):
  prefix        = CharField(primary_key=True)
  pid           = ForeignKeyField(Program, related_name='subjects')
  webname       = TextField()
  
class BannerSchedule(dbModel):
  letter        = CharField()
  days          = CharField()
  startTime     = TimeField()
  endTime       = TimeField()
  sid           = CharField(primary_key = True)
  order         = IntegerField(unique = True)

class BannerCourses(dbModel):
  reFID         = PrimaryKeyField()
  subject       = ForeignKeyField(Subject)
  number        = CharField(null = False)
  section       = CharField(null = True)
  ctitle        = CharField(null = False)

class Term(dbModel):
  termCode          = IntegerField(primary_key = True)     #This line will result in an autoincremented number, which will not allow us to enter in our own code
  name              = CharField()
  editable          = BooleanField()
  

class Course(dbModel):
  cId               = PrimaryKeyField()
  prefix            = ForeignKeyField(Subject)
  bannerRef         = ForeignKeyField(BannerCourses)
  term              = ForeignKeyField(Term, null = False)
  schedule          = ForeignKeyField(BannerSchedule, null = False)
  capacity          = IntegerField(null = False, default=0)
  specialTopicName  = CharField(null = True)
  notes             = TextField(null = False)
  lastEditBy        = CharField(null = True)

class ProgramChair(dbModel):
  username     = ForeignKeyField(User)
  pid          = ForeignKeyField(Program)

class DivisionChair(dbModel):
  username     = ForeignKeyField(User)
  did          = ForeignKeyField(Division)

class InstructorCourse(dbModel):
  username     = ForeignKeyField(User)
  course       = ForeignKeyField(Course)
  
class Deadline(dbModel):
  term         = ForeignKeyField(Term)
  description  = TextField()
  date         = DateField()
  
class CourseChange(dbModel):
  cId               = IntegerField(primary_key = True)
  prefix            = ForeignKeyField(Subject)
  bannerRef         = ForeignKeyField(BannerCourses)
  term              = ForeignKeyField(Term, null = False)
  schedule          = ForeignKeyField(BannerSchedule, null = False)
  capacity          = IntegerField(null = False)
  specialTopicName  = CharField(null = True)
  notes             = TextField(null = False)
  lastEditBy        = CharField(null = True)
  changeType        = CharField(null = True)
  verified          = BooleanField(default = False)
  
class InstructorCourseChange(dbModel):
  username     = ForeignKeyField(User)
  course       = ForeignKeyField(CourseChange)
  


