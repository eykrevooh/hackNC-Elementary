from app.allImports import *
import os


class AuthorizedUser:

    '''
    initializes the authorized user class
    @param username - name of the user accessing the information
    @param prefix   - prefix of the subject being accessed
    '''

    def __init__(self, prefix = None):
        # @private
        self.username = authUser(request.environ)
        self.prefix = prefix

    '''
    returns the username of the user
    '''
    def getUsername(self):
        return self.username
        
        
    '''
    checks to see if the user is an admin
    @public
    '''

    def isAdmin(self):
        try:
            user = User.get(User.username == self.username)
            return user.isAdmin
        except:
            self.not_user()
            return None

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
        
    def not_user(self):
        attrDict = dict
        attrKeys = ['cn', 'description', 'displayName', 'eppn', 'givenName', 'mail', 'sn']
        for key in attrKeys:
            attrDict[key] = os.environ[key]
        return attrDict
