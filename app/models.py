from peewee import *
import os

# Create a database
from app.loadConfig import *
here = os.path.dirname(__file__)
cfg       = load_config(os.path.join(here, 'config.yaml'))
db	  = os.path.join(here,'../',cfg['databases']['dev']) 
# mainDB    = SqliteDatabase(cfg['databases']['dev'])
mainDB    = SqliteDatabase(db,
                          pragmas = ( ('busy_timeout',  100),
                                      ('journal_mode', 'WAL')
                                  ),
                          threadlocals = True
                          )

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


#MODELS WITHOUT A FOREIGN KEY
class Division(dbModel):
  dID           = PrimaryKeyField()
  name          = CharField()
  
class BannerSchedule(dbModel):
  letter        = CharField()
  days          = CharField(null = True)
  startTime     = TimeField(null = True)
  endTime       = TimeField(null = True)
  sid           = CharField(primary_key = True)
  order         = IntegerField(unique = True)

class Term(dbModel):
  termCode          = IntegerField(primary_key = True)     #This line will result in an autoincremented number, which will not allow us to enter in our own code
  semester          = CharField(null = True)
  year              = IntegerField(null = True)
  name              = CharField()
  editable          = BooleanField()
  
class Rooms(dbModel):
  rID            = PrimaryKeyField()
  building       = CharField(null=False)
  number         = CharField(null=False)
  maxCapacity    = IntegerField(null=True)
  roomType       = CharField(null=False)
  
#MODELS WITH A FOREIGN KEY
class Program(dbModel):
  pID           = PrimaryKeyField()
  name          = CharField()
  division      = ForeignKeyField(Division)

class Subject(dbModel):
  prefix        = CharField(primary_key=True)
  pid           = ForeignKeyField(Program, related_name='subjects')
  webname       = TextField()

class User(dbModel):
  username     = CharField(primary_key=True)
  firstName    = CharField()
  lastName     = CharField()
  email        = CharField()
  isAdmin      = BooleanField()
  lastVisited  = ForeignKeyField(Subject, null=True)
  
class BannerCourses(dbModel):
  reFID         = PrimaryKeyField()
  subject       = ForeignKeyField(Subject)
  number        = CharField(null = False)
  section       = CharField(null = True)
  ctitle        = CharField(null = False)

class Course(dbModel):
  cId               = PrimaryKeyField()
  prefix            = ForeignKeyField(Subject)
  bannerRef         = ForeignKeyField(BannerCourses)
  term              = ForeignKeyField(Term, null = False)
  schedule          = ForeignKeyField(BannerSchedule, null = True)
  capacity          = IntegerField(null = True)
  specialTopicName  = CharField(null = True)
  notes             = TextField(null = True)
  lastEditBy        = CharField(null = True)
  crossListed       = BooleanField()
  rid               = ForeignKeyField(Rooms, null = True)

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
  description  = TextField()
  date         = DateField()
  
class CourseChange(dbModel):
  cId               = IntegerField(primary_key = True)
  prefix            = ForeignKeyField(Subject)
  bannerRef         = ForeignKeyField(BannerCourses)
  term              = ForeignKeyField(Term, null = False)
  schedule          = ForeignKeyField(BannerSchedule, null = True)
  capacity          = IntegerField(null = True)
  specialTopicName  = CharField(null = True)
  notes             = TextField(null = True)
  lastEditBy        = CharField(null = True)
  changeType        = CharField(null = True)
  verified          = BooleanField(default = False)
  crossListed       = BooleanField()
  rid               = ForeignKeyField(Rooms, null = True)
  tdcolors          = CharField(null = False)
  
class InstructorCourseChange(dbModel):
  username     = ForeignKeyField(User)
  course       = ForeignKeyField(CourseChange)
  
class CoursesInBanner(dbModel):
  CIBID        = PrimaryKeyField()
  bannerRef    = ForeignKeyField(BannerCourses)
  instructor   = ForeignKeyField(User, null=True)

