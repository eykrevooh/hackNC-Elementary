import xlsxwriter
from app.allImports import *


def makeExcelFile(term):
    workbook = xlsxwriter.Workbook('cas-{}-courses.xlsx'.format(term.termCode))
    workbook.set_properties({
    'title':    'Course Schedule for {}'.format(term.name),
    'author':   'Cas System',
    'comments': 'Created with Python and XlsxWriter'})
    
    # create a master worksheet
    master_worksheet = workbook.add_worksheet('All Courses')
    row = 2
    master_row = 2
    subjects = Subject.select().order_by(Subject.prefix)
    # add values 
    master_worksheet.write('A1','Prefix')
    master_worksheet.write('B1','Number')
    master_worksheet.write('C1','Title')
    master_worksheet.write('D1','Block ID')
    master_worksheet.write('E1','Block')
    master_worksheet.write('F1', 'Capacity')
    
    #loop though the subjects
    for subject in subjects:
        row = 2
        current_sheet = workbook.add_worksheet(subject.prefix)
        current_sheet.write('A1','Prefix')
        current_sheet.write('B1','Number')
        current_sheet.write('C1','Title')
        current_sheet.write('D1','Block ID')
        current_sheet.write('E1','Block')
        current_sheet.write('F1', 'Capacity')
        
        courses = Course.select().where(Course.prefix == subject.prefix).where(Course.term == term).order_by(Course.bannerRef)
        
        for course in courses:
            
            
            master_worksheet.write('A{}'.format(master_row), course.prefix.prefix)
            master_worksheet.write('B{}'.format(master_row), course.bannerRef.number)
            master_worksheet.write('C{}'.format(master_row), course.bannerRef.ctitle)
            if course.schedule is not None:
                master_worksheet.write('D{}'.format(master_row), course.schedule.sid)
                master_worksheet.write('E{}'.format(master_row), course.schedule.letter)
                current_sheet.write('D{}'.format(row), course.schedule.sid)
                current_sheet.write('E{}'.format(row), course.schedule.letter)
            master_worksheet.write('F{}'.format(master_row), course.capacity)
            
            current_sheet.write('A{}'.format(row), course.prefix.prefix)
            current_sheet.write('B{}'.format(row), course.bannerRef.number)
            current_sheet.write('C{}'.format(row), course.bannerRef.ctitle)
            
            current_sheet.write('F{}'.format(row), course.capacity)
            
            instructors = InstructorCourse.select().where(InstructorCourse.course == course.cId)
            colNum = ord('G')
            for instructor in instructors:
                master_worksheet.write('{0}{1}'.format(chr(colNum), master_row), instructor.username.username)
                current_sheet.write('{0}{1}'.format(chr(colNum), row), instructor.username.username)
                colNum += 1
            row += 1
            master_row += 1
            
    workbook.close()