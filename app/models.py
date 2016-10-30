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
class User(dbModel):
  uID           = PrimaryKeyField()
  username      = TextField()
  name          = TextField()
  password      = TextField()
  role          = IntegerField()
  year          = IntegerField()
  sex           = IntegerField()
  race          = TextField()

  def __str__(self):
    return str(self.name)


class Ta(dbModel):
    taID        = PrimaryKeyField()
    uID         = ForeignKeyField(User)
    bio         = TextField()
    pict        = TextField()
    working     = IntegerField()

    def __str__(self):
        return str(self.name)

class Student(dbModel):
    sID         = PrimaryKeyField()
    uID         = ForeignKeyField(User)
    need_help   = IntegerField()

    def __str__(self):
        return str(self.name)

class Course(dbModel):
    cID         = PrimaryKeyField()
    course_num  = TextField()
    course_title= TextField()
    course_dec  = TextField()
    python      = IntegerField()
    c           = IntegerField()
    cplus       = IntegerField()
    c_sharp     = IntegerField()
    java        = IntegerField()
    racket      = IntegerField()
    haskell     = IntegerField()

    def __str__(self):
        return str(self.name)

class Question(dbModel):
    qID         = PrimaryKeyField()
    sID         = ForeignKeyField(Student)
    cID         = ForeignKeyField(Course)
    taID        = ForeignKeyField(Ta, default=0)
    status      = TextField()
    assignment  = TextField()
    title       = TextField()
    question    = TextField()

    def __str__(self):
        return str(self.name)

class SCRelation(dbModel):
    scrID       = PrimaryKeyField()
    sID         = ForeignKeyField(Student)
    cID         = ForeignKeyField(Course)

    def __str__(self):
        return str(self.name)

class TaCRelation(dbModel):
    tacID       = PrimaryKeyField()
    taID        = ForeignKeyField(Ta)
    cID         = ForeignKeyField(Course)

    def __str__(self):
        return str(self.name)

