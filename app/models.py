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
  food          = CharField()

  def __str__(self):
    return str(self.name)
