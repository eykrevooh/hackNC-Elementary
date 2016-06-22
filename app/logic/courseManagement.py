#ADD ANY IMPORTS H
def crossListed():
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    crossListedCourses = Course.select().where(Course.crossListed == 1).order_by(+Course.schedule).order_by(+Course.rid)
  return crossListed()