from app.models import *
import MySQLdb
import datetime
# this function populates the database with the information found in the old system of cas
# change this to cas server if working outside of c9
try: 
  db = MySQLdb.connect(host = '127.0.0.1',
                       user = 'memo3301791',
                       passwd = '',
                       db     = 'c9',
                       port = 3306)
except:
  db = MySQLdb.connect(host = '127.0.0.1',
                       user = 'cody_myers',
                       passwd = '',
                       db     = 'c9',
                       port = 3306)
                     
cur = db.cursor()
#This updates the division
cur.execute("SELECT * FROM division")
for row in cur.fetchall():
  # print row[1]
  division = Division(dID = row[0],
                      name = row[1])
  division.save(force_insert= True)  

#this updates the programs

cur.execute("select * FROM program")

for row in cur.fetchall():
  # print row[1], row[3]
  program = Program(pID = row[0],
                      name = row[1],
                    division = row[3])
  program.save(force_insert = True)

cur.execute("SELECT * FROM userprofile")

for row in cur.fetchall():
  # print row[0], row[1], row[2], row[3], row[4]
  admin = 0
  if int(row[5]) == 4:
    admin = 1
  users = User(username = row[0],
              firstName = row[1],
              lastName = row[2],
              email    = row[3],
              isAdmin  = admin,
              lastVisted = None)
              
  users.save(force_insert = True)

# This will update the subjects
cur.execute("SELECT * FROM subjects")

for row in cur.fetchall():
  # print row[0], row[1], row[2]
  subject = Subject(prefix  = row[0],
                    pid     = int(row[1]),
                    webname = row[2])
  subject.save(force_insert = True)
# this updates the bannerCourses
cur.execute("select * from bannerschedules")

for row in cur.fetchall():
  # print row[0], row[1], row[2], row[3], row[4], row[5]
  schedule = BannerSchedule(letter = row[0],
                            days   = row[1],
                            startTime = (datetime.datetime.min + row[2]).time(),
                            endTime = (datetime.datetime.min + row[3]).time(),
                            sid = row[4],
                            order = int(row[5])).save(force_insert=True)
#this populates the banner courses
cur.execute("select * from bannercourses")

for row in cur.fetchall():
  # print row[0], row[1], row[2], row[4]
  bannercourse = BannerCourses(reFID = row[0],
                                subject = row[1],
                                number = row[2],
                                ctitle = row[4]).save(force_insert= True)
                                
# this gets the terms
cur.execute("select * from term")

for row in cur.fetchall():
  # print row[0], row[1], row[2], row[3]
  term = Term(name = row[1],
              termCode = row[2],
              editable = row[3]).save(force_insert=True)
              
# This populates the courses
cur.execute("select * from course")
cur2 = db.cursor()


for row in cur.fetchall():
  #print row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]
  cur2.execute("select subject from bannercourses where refID = {0}".format(row[1]))
  for subject in cur2.fetchall():
    sub = subject[0]
    
  cur2.execute("select term_code from term where TID = {}".format(row[2]))
  for term in cur2.fetchall():
    termCode = term[0]
  capacity = row[4]
  # if row[4] is None:
    # capacity = 0
  schedule = row[3]
  # if row[3] is None:
    # schedule = 'ZZZ'
  room = row[9]
  # if row[9] is None:
    # room = ''
  print row[0]
  course = Course(cId = int(row[0]),
                  bannerRef = int(row[1]),
                  term = int(termCode),
                  schedule = schedule,
                  capacity = capacity,
                  specialTopicName = row[6],
                  notes = room,
                  lastEditBy = row[10],
                  crossListed = 0,
                  prefix = str(sub)).save(force_insert = True) 
# this populates the programs
cur.execute("select * from program")
cur3 = db.cursor()
for row in cur.fetchall():
  cur3.execute("select username from userprofile where UID = {}".format(row[2]))
  for user in cur3.fetchall():
    username = user[0]
  # print row[1], username
  programChair = ProgramChair(username = username,
                              pid = row[0]).save()
# this populates the divisions                             
cur.execute("select * from division")
cur4 = db.cursor()
for row in cur.fetchall():
  cur4.execute("select username from userprofile where UID = {}".format(row[2]))
  for user in cur4.fetchall():
    username = user[0]
  # print row[1], username
  divisionChair = DivisionChair(username = username,
                                did   = row[0]).save()
# this populates the instructs
cur.execute("select * from instructors2")
cur5 = db.cursor()
for row in cur.fetchall():
  cur5.execute("select username from userprofile where UID = {}".format(row[1]))
  for user in cur5.fetchall():
    username = user[0]
  instructorCourse = InstructorCourse(username = username,
                                      course = row[2]).save()
                                      
cur.execute("select * from rooms")
for row in cur.fetchall():
  room = Rooms(rID = row[0],
              building = row[1],
              number = row[2],
              maxCapacity = row[3],
              roomType = row[4]).save(force_insert = True)
                            
db.close()

