from app.models import *
import csv
import re

# try to create the table
try:
  CoursesInBanner.create_table()
except:
  print "tablee probably already exists"
# csv has all the courses
with open('Book2.csv', 'rb') as csvfile:
  courses = csv.reader(csvfile)
  
  # disregard first entry its a header
  next(courses)
  for course in courses:
    print course[1], course[2], course[3], course[9], course[8]
    #number = int(re.search(r'\d+', course[2]).group())
    number = course[2]
    bannerRef = (BannerCourses.select().where(BannerCourses.subject == course[1])
                                       .where(BannerCourses.number == number))
    if bannerRef.exists():
      print 'found banner ref'
    else:
      number = int(re.search(r'\d+', course[2]).group())
      bannerRef = (BannerCourses.select().where(BannerCourses.subject == course[1])
                                       .where(BannerCourses.number == number))
      
       # these courses only have one instructor this may change 
    # in the future
    instructor = (User.select().where(User.firstName == course[9])
                              .where(User.lastName == course[8]))

    if instructor.exists():
      instructorUsername = instructor[0].username
    else:
      instructorUsername = None
    courseInBanner = CoursesInBanner(bannerRef = bannerRef[0].reFID,
                                     instructor = instructorUsername)
    courseInBanner.save()

                                     
