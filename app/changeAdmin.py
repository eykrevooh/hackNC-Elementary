from allImports import *
@app.route("/changeAdmin", methods=["POST"])
def changeAdmin():
    username = authUser(request.environ)
    admin = User.get(User.username == username)
    if admin.isAdmin:
      data = request.form
      print data
      user = User.get(User.username == data['admin'])
      user.isAdmin = not user.isAdmin
      user.save()  
    return "hello"