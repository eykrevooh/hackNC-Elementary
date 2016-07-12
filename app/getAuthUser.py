from allImports import *


class AuthorizedUser:

    '''
    initializes the authorized user class
    @param username - name of the user accessing the information
    @param prefix   - prefix of the subject being accessed
    '''

    def __init__(self, username, prefix = None):
        # @private
        self.username = username
        self.prefix = prefix

    '''
    checks to see if the user is an admin
    @public
    '''

    def isAdmin(self):
        user = User.get(User.username == self.username)
        return user.isAdmin

    '''
    check to see if the user is a division chair
    @private
    '''

    def isDivisionChair(self):
        subject = self.getSubject()

        return DivisionChair.select().where(
            DivisionChair.username == self.username).where(
            DivisionChair.did == subject.pid.division.dID).exists()

    '''
    check to see if the user is program chair
    @private
    '''

    def isProgramChair(self):
        subject = self.getSubject()

        return ProgramChair.select().where(
            ProgramChair.username == self.username).where(
            ProgramChair.pid == subject.pid.pID).exists()
    '''
    gets the subject we are trying to get
    @private
    '''

    def getSubject(self):
        return Subject.get(Subject.prefix == self.prefix)

    '''
    checks to see if user is program chair, admin, or division chair
    @public
    '''

    def isAuthorized(self):
        isAdminBool = self.isAdmin()
        isProgramChairBool = self.isProgramChair()
        isDivisionChairBool = self.isDivisionChair()
        return(isAdminBool or isProgramChairBool or isDivisionChairBool)
