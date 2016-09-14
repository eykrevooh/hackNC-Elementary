from app.models import *
import csv 

selectedTerm = 201612
BannerRefs = Course.select(Course.bannerRef).where(Course.term==selectedTerm).distinct()
differences = []
for ref in BannerRefs:
    REF = ref.bannerRef.reFID
    checkCourses = (Course.select().where(Course.term==selectedTerm)
                    .where(Course.bannerRef == REF))
    checkCourseInBanner = (CoursesInBanner.select().where(CoursesInBanner.bannerRef == REF))
    
    numInCAS   = checkCourses.count()
    numInCSV   = checkCourseInBanner.count()
    
    if numInCAS != numInCSV:
        bannerInfo = BannerCourses.get(BannerCourses.reFID == REF)
        prefix     = bannerInfo.subject.prefix
        number     = bannerInfo.number
        title      = bannerInfo.ctitle
        '''Test Prints'''
        #print "MISMATCH [bannerRef({0})]: course table has [{1}], excel sheet has [{2}]".format(REF,numInCAS,numInCSV)
        
        #print "{0} {1} - {2}".format(prefix,number,title)
        #print "\n"
        ''' structure: [prefix,number,title,#inCAS,#inExcel]'''
        mismatch = (str(prefix),str(number),str(title),str(numInCAS),str(numInCSV))
        differences.append(mismatch)
    else:
        #print "bannerRef {} okay".format(ref.bannerRef.reFID)
        #print "The number of bannerRef ({0})for semester ({1}) == the number in courseinbanner".format(ref.bannerRef.reFID,selectedTerm)
        pass
try:
    f = open('Differences.csv','wt')
    writer = csv.writer(f)
    writer.writerow( ('prefix','number','title','# in CAS', '# in Excel'))
    for mismatch in differences:
        writer.writerow(mismatch)
except Exception as e:
    print e
    
finally:
    f.close
        
        
        