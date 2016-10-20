from app.models import *
import csv
import re

# try to create the table
try:
  CoursesInBanner.create_table()
except:
  print "tablee probably already exists"
# csv has all the courses
problems = []
with open('Book3.csv', 'rb') as csvfile:
  courses = csv.reader(csvfile)
  
  # disregard first entry its a header
  next(courses)
  for course in courses:
    # Find and put their column location in the csv here
    ## Course Info ##
    TID         = course[0]
    subject     = course[1]
    number      = course[2]
    CRN         = course[9]
    location    = None
    title       = course[4]
    ## Course Instructor Info ##
    firstName   = course[7]
    lastName    = course[8]
    print CRN, subject, number, firstName, lastName 
    
    bannerRef = (BannerCourses.select().where(BannerCourses.subject == subject)
                                       .where(BannerCourses.number == number))
    if bannerRef.exists():
      print 'found banner ref'
    else:
      bannerRef = None
      issue = (str(CRN),str(subject),str(number),str(title))
      problems.append(issue)
    if bannerRef != None:
      instructor = (User.select().where(User.firstName == firstName)
                              .where(User.lastName == lastName))
      if instructor.exists():
        instructorUsername = instructor[0].username
      else:
        instructorUsername = None
      courseInBanner = CoursesInBanner(bannerRef = bannerRef[0].reFID,
                                        instructor = instructorUsername)
      courseInBanner.save()
  try:
    f = open('Problems.csv','wt')
    writer = csv.writer(f)
    writer.writerow(('CRN','subject','number','title'))
    for issue in problems:
        writer.writerow(issue)
  except Exception as e:
    print e

                                     
