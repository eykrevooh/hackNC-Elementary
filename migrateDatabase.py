from app.models import *
import MySQLdb
import datetime


db = MySQLdb.connect(host = '127.0.0.1',
                     user = 'agarwali',
                     passwd = '',
                     db     = 'c9',
                     port = 3306)
                     
cur = db.cursor()
# This updates the division
# cur.execute("SELECT * FROM division")
# for row in cur.fetchall():
# print row[1]
# division = Division(name = row[1])
# division.save()  

#this updates the programs

# cur.execute("select * FROM program")

# for row in cur.fetchall():
#   print row[1], row[3]
#   program = Program(name = row[1],
#                     division = row[3])
#   program.save()

# cur.execute("SELECT * FROM userprofile")

# for row in cur.fetchall():
#   print row[0], row[1], row[2], row[3], row[4]
#   admin = 0
#   if int(row[5]) == 4:
#     admin = 1
#   users = User(username = row[0],
#               firstName = row[1],
#               lastName = row[2],
#               email    = row[3],
#               isAdmin  = admin,
#               program = row[4])
              
#   users.save(force_insert = True)

# This will update the subjects
# cur.execute("SELECT * FROM subjects")

# for row in cur.fetchall():
#   print row[0], row[1], row[2]
#   subject = Subject(prefix  = row[0],
#                     pid     = int(row[1]),
#                     webname = row[2])
#   subject.save(force_insert = True)

cur.execute("select * from bannerschedules")

for row in cur.fetchall():
  print row[0], row[1], row[2], row[3], row[4], row[5]
  # schedule = BannerSchedule(letter = row[0],
  #                           days   = row[1],
  #                           startTime = row[2],
  #                           endTime = row[3],
  #                           sid = row[4],
  #                           order = int(row[5])).save()
  print type(row[2])
  print type((datetime.datetime.min + row[2]).time())
db.close()

