from allImports import *
from flask_admin.contrib.peewee import ModelView

class AuthenticatedUser(ModelView):
    
    def is_accessible(self):
        return authUser(request.environ) == cfg['databaseAdmin']['user']
    
admin.add_view(AuthenticatedUser(Division))
admin.add_view(AuthenticatedUser(BannerSchedule))
admin.add_view(AuthenticatedUser(Term))
admin.add_view(AuthenticatedUser(Rooms))
admin.add_view(AuthenticatedUser(Program))
admin.add_view(AuthenticatedUser(Subject))
admin.add_view(AuthenticatedUser(User))

admin.add_view(AuthenticatedUser(BannerCourses))
admin.add_view(AuthenticatedUser(Course))
admin.add_view(AuthenticatedUser(ProgramChair))
admin.add_view(AuthenticatedUser(DivisionChair))
admin.add_view(AuthenticatedUser(InstructorCourse))
admin.add_view(AuthenticatedUser(Deadline))

admin.add_view(AuthenticatedUser(CourseChange))
admin.add_view(AuthenticatedUser(InstructorCourseChange))